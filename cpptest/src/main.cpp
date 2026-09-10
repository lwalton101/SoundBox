// CD player test UI for Raspberry Pi 3B (VideoCore IV / OpenGL ES 2).
//
// Pi build:
//   sudo apt install build-essential pkg-config libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev
//   make
//   ./cdplayer
//   ./cdplayer --fullscreen
//
// Keys: Esc quit, F toggle FPS, F11 fullscreen.

#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>

#ifdef __linux__
#include <unistd.h>
#endif

#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>

namespace {

constexpr int kWidth = 1280;
constexpr int kHeight = 800;
constexpr int kTargetFps = 60;

constexpr float kDiscSizePx = 460.0f;
constexpr double kSpinRpm = 33.333;
constexpr double kDegPerSec = kSpinRpm * 360.0 / 60.0;
constexpr double kIntroSeconds = 1.35;
constexpr double kIntroExtraSpin = 420.0;

constexpr double kSongSeconds = 3 * 60.0 + 56.0;  // Alexander Hamilton
const char* kSongTitle = "Alexander Hamilton";
const char* kAlbumLine = "Hamilton (Original Broadway Cast)";

constexpr SDL_Color kBg{18, 16, 14, 255};
constexpr SDL_Color kTitle{242, 239, 232, 255};
constexpr SDL_Color kMuted{168, 158, 145, 255};
constexpr SDL_Color kBarTrack{48, 42, 36, 255};
constexpr SDL_Color kBarFill{196, 163, 90, 255};

struct Texture {
    SDL_Texture* ptr = nullptr;
    int w = 0;
    int h = 0;

    void destroy() {
        if (ptr) {
            SDL_DestroyTexture(ptr);
            ptr = nullptr;
        }
    }
};

std::string dirnameOf(const std::string& path) {
    const auto slash = path.find_last_of("/\\");
    if (slash == std::string::npos) {
        return ".";
    }
    return path.substr(0, slash);
}

std::string executableDir(char* argv0) {
#ifdef __linux__
    char buf[4096];
    const ssize_t n = readlink("/proc/self/exe", buf, sizeof(buf) - 1);
    if (n > 0) {
        buf[n] = '\0';
        return dirnameOf(buf);
    }
#endif
    if (argv0 && argv0[0]) {
        return dirnameOf(argv0);
    }
    return ".";
}

bool fileExists(const std::string& path) {
    SDL_RWops* rw = SDL_RWFromFile(path.c_str(), "rb");
    if (!rw) {
        return false;
    }
    SDL_RWclose(rw);
    return true;
}

std::string firstExisting(const std::vector<std::string>& paths) {
    for (const auto& p : paths) {
        if (fileExists(p)) {
            return p;
        }
    }
    return {};
}

double nowSeconds() {
    return static_cast<double>(SDL_GetPerformanceCounter()) /
           static_cast<double>(SDL_GetPerformanceFrequency());
}

float easeOutCubic(float t) {
    t = std::clamp(t, 0.0f, 1.0f);
    const float inv = 1.0f - t;
    return 1.0f - inv * inv * inv;
}

SDL_BlendMode premultipliedBlend() {
#if SDL_VERSION_ATLEAST(2, 0, 12)
    return SDL_ComposeCustomBlendMode(
        SDL_BLENDFACTOR_ONE,
        SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
        SDL_BLENDOPERATION_ADD,
        SDL_BLENDFACTOR_ONE,
        SDL_BLENDFACTOR_ONE_MINUS_SRC_ALPHA,
        SDL_BLENDOPERATION_ADD);
#else
    return SDL_BLENDMODE_BLEND;
#endif
}

Texture loadTexturePremul(SDL_Renderer* renderer, const std::string& path) {
    Texture out;
    SDL_Surface* loaded = IMG_Load(path.c_str());
    if (!loaded) {
        std::fprintf(stderr, "IMG_Load failed (%s): %s\n", path.c_str(), IMG_GetError());
        return out;
    }

    SDL_Surface* rgba = SDL_ConvertSurfaceFormat(loaded, SDL_PIXELFORMAT_RGBA32, 0);
    SDL_FreeSurface(loaded);
    if (!rgba) {
        std::fprintf(stderr, "ConvertSurfaceFormat failed: %s\n", SDL_GetError());
        return out;
    }

    SDL_LockSurface(rgba);
    auto* pixels = static_cast<Uint8*>(rgba->pixels);
    for (int y = 0; y < rgba->h; ++y) {
        Uint8* row = pixels + y * rgba->pitch;
        for (int x = 0; x < rgba->w; ++x) {
            Uint8* p = row + x * 4;
            const unsigned a = p[3];
            p[0] = static_cast<Uint8>(p[0] * a / 255u);
            p[1] = static_cast<Uint8>(p[1] * a / 255u);
            p[2] = static_cast<Uint8>(p[2] * a / 255u);
        }
    }
    SDL_UnlockSurface(rgba);

    out.ptr = SDL_CreateTextureFromSurface(renderer, rgba);
    out.w = rgba->w;
    out.h = rgba->h;
    SDL_FreeSurface(rgba);

    if (!out.ptr) {
        std::fprintf(stderr, "CreateTextureFromSurface failed: %s\n", SDL_GetError());
        return out;
    }

    SDL_SetTextureBlendMode(out.ptr, premultipliedBlend());
#if SDL_VERSION_ATLEAST(2, 0, 12)
    SDL_SetTextureScaleMode(out.ptr, SDL_ScaleModeLinear);
#endif
    return out;
}

Texture bakeText(SDL_Renderer* renderer, TTF_Font* font, const char* text, SDL_Color color) {
    Texture out;
    if (!font || !text || !text[0]) {
        return out;
    }
    SDL_Surface* surface = TTF_RenderUTF8_Blended(font, text, color);
    if (!surface) {
        std::fprintf(stderr, "TTF_RenderUTF8_Blended failed: %s\n", TTF_GetError());
        return out;
    }
    out.ptr = SDL_CreateTextureFromSurface(renderer, surface);
    out.w = surface->w;
    out.h = surface->h;
    SDL_FreeSurface(surface);
    if (out.ptr) {
        SDL_SetTextureBlendMode(out.ptr, SDL_BLENDMODE_BLEND);
#if SDL_VERSION_ATLEAST(2, 0, 12)
        SDL_SetTextureScaleMode(out.ptr, SDL_ScaleModeLinear);
#endif
    }
    return out;
}

void drawTexture(SDL_Renderer* renderer, const Texture& tex, float x, float y) {
    if (!tex.ptr) {
        return;
    }
    SDL_FRect dst{x, y, static_cast<float>(tex.w), static_cast<float>(tex.h)};
    SDL_RenderCopyF(renderer, tex.ptr, nullptr, &dst);
}

void fillF(SDL_Renderer* renderer, float x, float y, float w, float h, SDL_Color c) {
    SDL_SetRenderDrawColor(renderer, c.r, c.g, c.b, c.a);
    SDL_FRect r{x, y, w, h};
    SDL_RenderFillRectF(renderer, &r);
}

std::string formatTime(double seconds) {
    seconds = std::clamp(seconds, 0.0, 99.0 * 60.0 + 59.0);
    const int total = static_cast<int>(seconds);
    const int m = total / 60;
    const int s = total % 60;
    char buf[16];
    std::snprintf(buf, sizeof(buf), "%d:%02d", m, s);
    return buf;
}

SDL_Window* createWindow(bool fullscreen, int samples) {
    if (samples > 0) {
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1);
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, samples);
    } else {
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 0);
        SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 0);
    }
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_RED_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_GREEN_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_BLUE_SIZE, 8);
    SDL_GL_SetAttribute(SDL_GL_ALPHA_SIZE, 8);

#if defined(__arm__) || defined(__aarch64__)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_ES);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 0);
#endif

    Uint32 flags = SDL_WINDOW_OPENGL | SDL_WINDOW_ALLOW_HIGHDPI;
    if (fullscreen) {
        flags |= SDL_WINDOW_FULLSCREEN;
    }

    return SDL_CreateWindow(
        "SoundBox CD Test",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        kWidth,
        kHeight,
        flags);
}

SDL_Renderer* createHardwareRenderer(SDL_Window* window) {
    SDL_Renderer* renderer = SDL_CreateRenderer(
        window,
        -1,
        SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer) {
        std::fprintf(stderr, "Accelerated vsync renderer failed: %s\n", SDL_GetError());
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    }
    return renderer;
}

bool printRendererInfo(SDL_Renderer* renderer) {
    SDL_RendererInfo info{};
    if (SDL_GetRendererInfo(renderer, &info) != 0) {
        return false;
    }
    const bool accelerated = (info.flags & SDL_RENDERER_ACCELERATED) != 0;
    const bool vsync = (info.flags & SDL_RENDERER_PRESENTVSYNC) != 0;
    std::printf(
        "SDL renderer: %s  accelerated=%s  vsync=%s  max_texture=%dx%d\n",
        info.name,
        accelerated ? "yes" : "NO (software)",
        vsync ? "yes" : "no",
        info.max_texture_width,
        info.max_texture_height);
    if (!accelerated) {
        std::fprintf(stderr, "Warning: falling back to software rendering.\n");
    }
    return vsync;
}

}  // namespace

int main(int argc, char* argv[]) {
    bool fullscreen = false;
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--fullscreen") == 0 || std::strcmp(argv[i], "-f") == 0) {
            fullscreen = true;
        }
    }

    SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "linear");
    SDL_SetHint(SDL_HINT_RENDER_BATCHING, "1");
    SDL_SetHint(SDL_HINT_RENDER_VSYNC, "1");
    SDL_SetHint(SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS, "0");
#if defined(__arm__) || defined(__aarch64__)
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, "opengles2");
#endif

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) != 0) {
        std::fprintf(stderr, "SDL_Init failed: %s\n", SDL_GetError());
        return 1;
    }
    if ((IMG_Init(IMG_INIT_PNG | IMG_INIT_JPG) & (IMG_INIT_PNG | IMG_INIT_JPG)) == 0) {
        std::fprintf(stderr, "IMG_Init failed: %s\n", IMG_GetError());
        SDL_Quit();
        return 1;
    }
    if (TTF_Init() != 0) {
        std::fprintf(stderr, "TTF_Init failed: %s\n", TTF_GetError());
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Window* window = nullptr;
    const int sampleTries[] = {4, 2, 0};
    for (int samples : sampleTries) {
        window = createWindow(fullscreen, samples);
        if (window) {
            std::printf("Created window with MSAA samples request: %d\n", samples);
            break;
        }
        std::fprintf(stderr, "Window create failed (MSAA %d): %s\n", samples, SDL_GetError());
    }
    if (!window) {
        TTF_Quit();
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    SDL_Renderer* renderer = createHardwareRenderer(window);
    if (!renderer) {
        std::fprintf(stderr, "SDL_CreateRenderer failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        TTF_Quit();
        IMG_Quit();
        SDL_Quit();
        return 1;
    }
    const bool hasVsync = printRendererInfo(renderer);
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
    SDL_RenderSetLogicalSize(renderer, kWidth, kHeight);
    SDL_RenderSetIntegerScale(renderer, SDL_FALSE);

    const std::string exeDir = executableDir(argc > 0 ? argv[0] : nullptr);
    const std::string discPath = firstExisting({
        exeDir + "/assets/hamilton-disc.png",
        "assets/hamilton-disc.png",
        "../assets/hamilton-disc.png",
        exeDir + "/../assets/hamilton-disc.png",
    });
    if (discPath.empty()) {
        std::fprintf(stderr, "Could not find assets/hamilton-disc.png\n");
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        TTF_Quit();
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    Texture disc = loadTexturePremul(renderer, discPath);
    if (!disc.ptr) {
        SDL_DestroyRenderer(renderer);
        SDL_DestroyWindow(window);
        TTF_Quit();
        IMG_Quit();
        SDL_Quit();
        return 1;
    }

    const std::string fontPath = firstExisting({
        exeDir + "/assets/DejaVuSans.ttf",
        "assets/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    });

    TTF_Font* titleFont = nullptr;
    TTF_Font* bodyFont = nullptr;
    TTF_Font* fpsFont = nullptr;
    if (!fontPath.empty()) {
        titleFont = TTF_OpenFont(fontPath.c_str(), 36);
        bodyFont = TTF_OpenFont(fontPath.c_str(), 20);
        fpsFont = TTF_OpenFont(fontPath.c_str(), 18);
        if (!titleFont) {
            std::fprintf(stderr, "TTF_OpenFont failed (%s): %s\n", fontPath.c_str(), TTF_GetError());
        }
    } else {
        std::fprintf(stderr, "No TTF font found; song title will be omitted.\n");
    }

    Texture titleTex = bakeText(renderer, titleFont, kSongTitle, kTitle);
    Texture albumTex = bakeText(renderer, bodyFont, kAlbumLine, kMuted);

    bool running = true;
    bool showFps = true;
    bool isFullscreen = fullscreen;
    const double start = nowSeconds();
    double fpsWindowStart = start;
    int fpsFrames = 0;
    float fpsDisplay = 0.0f;
    Texture fpsTex;
    Texture timeTex;
    int lastShownSecond = -1;

    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                running = false;
            } else if (event.type == SDL_KEYDOWN && event.key.repeat == 0) {
                if (event.key.keysym.sym == SDLK_ESCAPE) {
                    running = false;
                } else if (event.key.keysym.sym == SDLK_f) {
                    showFps = !showFps;
                } else if (event.key.keysym.sym == SDLK_F11) {
                    isFullscreen = !isFullscreen;
                    SDL_SetWindowFullscreen(
                        window,
                        isFullscreen ? SDL_WINDOW_FULLSCREEN : 0);
                }
            }
        }

        const double t = nowSeconds() - start;
        const float intro = easeOutCubic(static_cast<float>(t / kIntroSeconds));
        const double spin = t * kDegPerSec + (1.0 - static_cast<double>(intro)) * kIntroExtraSpin;
        const double angle = std::fmod(spin, 360.0);
        const float scale = 0.18f + 0.82f * intro;

        const double progressT = std::fmod(t, kSongSeconds);
        const float progress = static_cast<float>(progressT / kSongSeconds);

        fpsFrames += 1;
        if (nowSeconds() - fpsWindowStart >= 0.5) {
            fpsDisplay = static_cast<float>(
                fpsFrames / (nowSeconds() - fpsWindowStart));
            fpsFrames = 0;
            fpsWindowStart = nowSeconds();
            if (showFps && fpsFont) {
                char buf[48];
                std::snprintf(buf, sizeof(buf), "%.0f fps", fpsDisplay);
                fpsTex.destroy();
                fpsTex = bakeText(renderer, fpsFont, buf, kMuted);
            }
        }

        const int shownSecond = static_cast<int>(progressT);
        if (shownSecond != lastShownSecond && bodyFont) {
            lastShownSecond = shownSecond;
            const std::string label = formatTime(progressT) + "  /  " + formatTime(kSongSeconds);
            timeTex.destroy();
            timeTex = bakeText(renderer, bodyFont, label.c_str(), kMuted);
        }

        SDL_SetRenderDrawColor(renderer, kBg.r, kBg.g, kBg.b, 255);
        SDL_RenderClear(renderer);

        const float discW = kDiscSizePx * scale;
        const float discH = kDiscSizePx * scale;
        const float discX = (kWidth - discW) * 0.5f;
        const float discY = 86.0f + (1.0f - intro) * 28.0f;

        SDL_FRect discDst{discX, discY, discW, discH};
        SDL_FPoint origin{discW * 0.5f, discH * 0.5f};

        SDL_FRect shadow = discDst;
        shadow.x += 10.0f;
        shadow.y += 16.0f;
        SDL_SetTextureColorMod(disc.ptr, 0, 0, 0);
        SDL_SetTextureAlphaMod(disc.ptr, 55);
        SDL_RenderCopyExF(renderer, disc.ptr, nullptr, &shadow, angle, &origin, SDL_FLIP_NONE);

        SDL_SetTextureColorMod(disc.ptr, 255, 255, 255);
        SDL_SetTextureAlphaMod(disc.ptr, 255);
        SDL_RenderCopyExF(renderer, disc.ptr, nullptr, &discDst, angle, &origin, SDL_FLIP_NONE);

        const float textY = discY + discH + 28.0f;
        if (titleTex.ptr) {
            drawTexture(renderer, titleTex, (kWidth - titleTex.w) * 0.5f, textY);
        }
        if (albumTex.ptr) {
            drawTexture(
                renderer,
                albumTex,
                (kWidth - albumTex.w) * 0.5f,
                textY + (titleTex.ptr ? titleTex.h + 6.0f : 0.0f));
        }

        const float barW = 640.0f;
        const float barH = 10.0f;
        const float barX = (kWidth - barW) * 0.5f;
        const float barY = textY + 92.0f;
        fillF(renderer, barX, barY, barW, barH, kBarTrack);
        fillF(renderer, barX, barY, barW * progress, barH, kBarFill);
        fillF(
            renderer,
            barX + barW * progress - 2.0f,
            barY - 3.0f,
            4.0f,
            barH + 6.0f,
            kTitle);

        if (timeTex.ptr) {
            drawTexture(renderer, timeTex, (kWidth - timeTex.w) * 0.5f, barY + 18.0f);
        }

        if (showFps && fpsTex.ptr) {
            drawTexture(renderer, fpsTex, 16.0f, 12.0f);
        }

        SDL_RenderPresent(renderer);

        if (!hasVsync) {
            static double lastFrame = nowSeconds();
            const double frameTime = 1.0 / static_cast<double>(kTargetFps);
            const double elapsed = nowSeconds() - lastFrame;
            if (elapsed < frameTime) {
                SDL_Delay(static_cast<Uint32>((frameTime - elapsed) * 1000.0));
            }
            lastFrame = nowSeconds();
        }
    }

    fpsTex.destroy();
    timeTex.destroy();
    titleTex.destroy();
    albumTex.destroy();
    disc.destroy();
    if (titleFont) {
        TTF_CloseFont(titleFont);
    }
    if (bodyFont) {
        TTF_CloseFont(bodyFont);
    }
    if (fpsFont) {
        TTF_CloseFont(fpsFont);
    }
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    TTF_Quit();
    IMG_Quit();
    SDL_Quit();
    return 0;
}
