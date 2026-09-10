CXX ?= g++
CXXFLAGS ?= -O2 -std=c++17 -Wall -Wextra
PKG_CFLAGS := $(shell pkg-config --cflags sdl2 SDL2_image SDL2_ttf)
PKG_LIBS := $(shell pkg-config --libs sdl2 SDL2_image SDL2_ttf)

.PHONY: all clean

all: cdplayer

cdplayer: src/main.cpp
	$(CXX) $(CXXFLAGS) $(PKG_CFLAGS) -o $@ $< $(PKG_LIBS)

clean:
	rm -f cdplayer
