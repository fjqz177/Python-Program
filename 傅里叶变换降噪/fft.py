import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_fourier_denoising(image, filter_size):
    f = np.fft.fft2(image)
    fshift = np.fft.fftshift(f)
    
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows,cols),np.uint8)
    mask[crow-filter_size:crow+filter_size, ccol-filter_size:ccol+filter_size] = 1
    
    fshift = fshift * mask
    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    return img_back

def denoise_color_image(image_path, filter_size):
    image = cv2.imread(image_path)

    b,g,r = cv2.split(image)
    
    denoised_channels = [apply_fourier_denoising(x, filter_size) for x in (b,g,r)]
    
    denoised_image = cv2.merge(denoised_channels)
    
    return denoised_image

image_path = "image.png"
filter_size = 255-100

denoised_image = denoise_color_image(image_path, filter_size)

original_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
denoised_image = cv2.cvtColor(cv2.normalize(denoised_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U), cv2.COLOR_BGR2RGB)

plt.figure(figsize=(12, 6))
plt.subplot(121), plt.imshow(original_image), plt.title('Original Image')
plt.subplot(122), plt.imshow(denoised_image), plt.title('Denoised Image')
plt.show()