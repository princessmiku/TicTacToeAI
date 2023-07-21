from PIL import Image, ImageDraw, ImageFilter

# Create an empty square image with white color
image_size = (300, 300)
img = Image.new('RGB', image_size, color=(255, 255, 255))
# Create Draw object
draw = ImageDraw.Draw(img)

# Create gradient
top_color = (50, 50, 50)  # Dark grey
bottom_color = (150, 150, 150)  # Light grey

for y in range(image_size[1]):
    for x in range(image_size[0]):
        # Here we calculate the ratio of the current y / height of the image
        r = float(y) / image_size[1]
        r = r ** 0.2  # You can tweak this exponent to get different curves for the gradient
        color = tuple([int(r * top_color[i] + (1-r) * bottom_color[i]) for i in range(3)])
        draw.point((x, y), fill=color)

# Draw the grid
line_color = (70, 130, 180, 255)
line_width = 3
draw = ImageDraw.Draw(img, 'RGBA')

for i in range(1, 3):
    # Vertical lines
    start_point = (i * image_size[0] // 3, 0)
    end_point = (i * image_size[0] // 3, image_size[1])
    draw.line([start_point, end_point], fill=line_color, width=line_width)

    # Horizontal lines
    start_point = (0, i * image_size[1] // 3)
    end_point = (image_size[0], i * image_size[1] // 3)
    draw.line([start_point, end_point], fill=line_color, width=line_width)

# Create a circular mask image
mask = Image.new('L', image_size)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((0, 0) + image_size, fill=255)

# Applied mask to original image
img.putalpha(mask)

# Save the image
img.save('logo.png')
img.resize((32,32))
img.save('logo.ico', format='ICO')
