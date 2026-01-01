"""
NeilerGPU: Custom GPU for Neiler Computer
Hardware-accelerated 2D graphics with sprites

Features:
- 320x200 resolution (8-bit mode) or 640x480 (16-bit mode)
- 256-color palette or 65K true color
- 64 hardware sprites (16x16 pixels)
- Tile-based backgrounds
- Hardware scrolling
- VBlank interrupts
"""

import numpy as np

class NeilerGPU:
    def __init__(self, mode='8bit'):
        self.mode = mode

        if mode == '8bit':
            self.width = 320
            self.height = 200
            self.colors = 256
        else:  # 16bit
            self.width = 640
            self.height = 480
            self.colors = 65536

        # Frame buffer
        self.framebuffer = np.zeros((self.height, self.width), dtype=np.uint16 if mode == '16bit' else np.uint8)

        # Palette (256 colors, RGB565 format)
        self.palette = np.zeros(256, dtype=np.uint16)
        self._init_default_palette()

        # Sprite system
        self.num_sprites = 64
        self.sprite_width = 16
        self.sprite_height = 16
        self.sprite_data = np.zeros((self.num_sprites, self.sprite_height, self.sprite_width), dtype=np.uint8)
        self.sprite_x = np.zeros(self.num_sprites, dtype=np.int16)
        self.sprite_y = np.zeros(self.num_sprites, dtype=np.int16)
        self.sprite_enabled = np.zeros(self.num_sprites, dtype=np.bool_)

        # Background layers
        self.bg_layer1 = np.zeros((self.height, self.width), dtype=np.uint8)
        self.bg_layer2 = np.zeros((self.height, self.width), dtype=np.uint8)
        self.bg1_scroll_x = 0
        self.bg1_scroll_y = 0
        self.bg2_scroll_x = 0
        self.bg2_scroll_y = 0

        # Registers (memory-mapped)
        self.registers = {
            'VBLANK': 0,      # VBlank flag
            'HBLANK': 0,      # HBlank flag
            'SPRITE_EN': 1,   # Sprites enabled
            'BG1_EN': 1,      # Background layer 1 enabled
            'BG2_EN': 0,      # Background layer 2 enabled
        }

        # Video RAM (8KB for sprites, 16KB for backgrounds)
        self.vram = bytearray(24 * 1024)

        # Frame counter
        self.frame_count = 0

    def _init_default_palette(self):
        """Initialize default color palette"""
        # Black to white gradient
        for i in range(256):
            r = g = b = i
            self.palette[i] = self.rgb_to_rgb565(r, g, b)

    @staticmethod
    def rgb_to_rgb565(r, g, b):
        """Convert RGB888 to RGB565"""
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

    @staticmethod
    def rgb565_to_rgb(color):
        """Convert RGB565 to RGB888 tuple"""
        r = ((color >> 11) & 0x1F) << 3
        g = ((color >> 5) & 0x3F) << 2
        b = (color & 0x1F) << 3
        return (r, g, b)

    def set_palette_color(self, index, r, g, b):
        """Set palette color (0-255, RGB values 0-255)"""
        self.palette[index] = self.rgb_to_rgb565(r, g, b)

    def set_pixel(self, x, y, color):
        """Set pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.framebuffer[y, x] = color

    def get_pixel(self, x, y):
        """Get pixel color"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.framebuffer[y, x]
        return 0

    def clear_screen(self, color=0):
        """Clear screen to color"""
        self.framebuffer.fill(color)

    def draw_line(self, x0, y0, x1, y1, color):
        """Draw line (Bresenham's algorithm)"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            self.set_pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def draw_rect(self, x, y, width, height, color, fill=False):
        """Draw rectangle"""
        if fill:
            for dy in range(height):
                for dx in range(width):
                    self.set_pixel(x + dx, y + dy, color)
        else:
            # Top and bottom
            for dx in range(width):
                self.set_pixel(x + dx, y, color)
                self.set_pixel(x + dx, y + height - 1, color)
            # Left and right
            for dy in range(height):
                self.set_pixel(x, y + dy, color)
                self.set_pixel(x + width - 1, y + dy, color)

    def draw_circle(self, cx, cy, radius, color, fill=False):
        """Draw circle (Midpoint circle algorithm)"""
        x = radius
        y = 0
        err = 0

        while x >= y:
            if fill:
                # Draw horizontal lines
                for dx in range(-x, x + 1):
                    self.set_pixel(cx + dx, cy + y, color)
                    self.set_pixel(cx + dx, cy - y, color)
                for dx in range(-y, y + 1):
                    self.set_pixel(cx + dx, cy + x, color)
                    self.set_pixel(cx + dx, cy - x, color)
            else:
                # Draw circle outline
                self.set_pixel(cx + x, cy + y, color)
                self.set_pixel(cx + y, cy + x, color)
                self.set_pixel(cx - y, cy + x, color)
                self.set_pixel(cx - x, cy + y, color)
                self.set_pixel(cx - x, cy - y, color)
                self.set_pixel(cx - y, cy - x, color)
                self.set_pixel(cx + y, cy - x, color)
                self.set_pixel(cx + x, cy - y, color)

            if err <= 0:
                y += 1
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    def load_sprite(self, sprite_id, sprite_data):
        """Load sprite data (16x16 pixels)"""
        if 0 <= sprite_id < self.num_sprites:
            self.sprite_data[sprite_id] = np.array(sprite_data).reshape((16, 16))

    def set_sprite_position(self, sprite_id, x, y):
        """Set sprite position"""
        if 0 <= sprite_id < self.num_sprites:
            self.sprite_x[sprite_id] = x
            self.sprite_y[sprite_id] = y

    def enable_sprite(self, sprite_id, enabled=True):
        """Enable/disable sprite"""
        if 0 <= sprite_id < self.num_sprites:
            self.sprite_enabled[sprite_id] = enabled

    def draw_sprite(self, sprite_id):
        """Draw sprite to framebuffer"""
        if not (0 <= sprite_id < self.num_sprites):
            return
        if not self.sprite_enabled[sprite_id]:
            return

        sx = self.sprite_x[sprite_id]
        sy = self.sprite_y[sprite_id]

        for y in range(self.sprite_height):
            for x in range(self.sprite_width):
                color = self.sprite_data[sprite_id, y, x]
                if color != 0:  # 0 is transparent
                    px = sx + x
                    py = sy + y
                    if 0 <= px < self.width and 0 <= py < self.height:
                        self.framebuffer[py, px] = color

    def draw_all_sprites(self):
        """Draw all enabled sprites"""
        for i in range(self.num_sprites):
            if self.sprite_enabled[i]:
                self.draw_sprite(i)

    def scroll_background(self, layer, dx, dy):
        """Scroll background layer"""
        if layer == 1:
            self.bg1_scroll_x = (self.bg1_scroll_x + dx) % self.width
            self.bg1_scroll_y = (self.bg1_scroll_y + dy) % self.height
        elif layer == 2:
            self.bg2_scroll_x = (self.bg2_scroll_x + dx) % self.width
            self.bg2_scroll_y = (self.bg2_scroll_y + dy) % self.height

    def render_background(self, layer):
        """Render background layer with scrolling"""
        if layer == 1 and self.registers['BG1_EN']:
            # Simple tile rendering with scroll offset
            for y in range(self.height):
                for x in range(self.width):
                    src_x = (x + self.bg1_scroll_x) % self.width
                    src_y = (y + self.bg1_scroll_y) % self.height
                    color = self.bg_layer1[src_y, src_x]
                    if color != 0:
                        self.framebuffer[y, x] = color

    def vsync(self):
        """Wait for vertical blank"""
        self.registers['VBLANK'] = 1
        self.frame_count += 1

    def get_framebuffer_rgb(self):
        """Get framebuffer as RGB array for display"""
        if self.mode == '8bit':
            # Convert palette indices to RGB
            rgb_buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for y in range(self.height):
                for x in range(self.width):
                    color_idx = self.framebuffer[y, x]
                    rgb = self.rgb565_to_rgb(self.palette[color_idx])
                    rgb_buffer[y, x] = rgb
            return rgb_buffer
        else:
            # 16-bit true color
            rgb_buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            for y in range(self.height):
                for x in range(self.width):
                    rgb = self.rgb565_to_rgb(self.framebuffer[y, x])
                    rgb_buffer[y, x] = rgb
            return rgb_buffer

    def blit_text(self, x, y, text, color, font_data=None):
        """Blit text to screen (simple 8x8 font)"""
        # Simple ASCII rendering (would need font data in real impl)
        char_width = 8
        char_height = 8

        for i, char in enumerate(text):
            char_x = x + i * char_width
            # Draw simple rectangle as placeholder
            self.draw_rect(char_x, y, char_width, char_height, color)


if __name__ == "__main__":
    # Test GPU
    gpu = NeilerGPU(mode='8bit')

    # Set up custom palette
    gpu.set_palette_color(1, 255, 0, 0)     # Red
    gpu.set_palette_color(2, 0, 255, 0)     # Green
    gpu.set_palette_color(3, 0, 0, 255)     # Blue
    gpu.set_palette_color(4, 255, 255, 0)   # Yellow

    # Draw some shapes
    gpu.clear_screen(0)
    gpu.draw_rect(10, 10, 50, 50, 1, fill=True)
    gpu.draw_circle(160, 100, 40, 2, fill=False)
    gpu.draw_line(0, 0, 319, 199, 3)

    # Create a simple sprite (smiley face)
    smiley = np.zeros((16, 16), dtype=np.uint8)
    # Yellow background
    smiley.fill(4)
    # Eyes
    smiley[5:7, 5:7] = 0
    smiley[5:7, 10:12] = 0
    # Smile
    smiley[10, 4:13] = 0
    smiley[11, 5:12] = 0

    gpu.load_sprite(0, smiley)
    gpu.set_sprite_position(0, 100, 100)
    gpu.enable_sprite(0)
    gpu.draw_sprite(0)

    print("GPU initialized and test render complete!")
    print(f"Resolution: {gpu.width}x{gpu.height}")
    print(f"Frame count: {gpu.frame_count}")
