
"""
Effects Processor Module

Handles all image processing operations using OpenCV.
Demonstrates OOP concepts: Inheritance, Polymorphism, Encapsulation.
"""

import numpy as np
import cv2
from typing import Optional, Dict, Any, Tuple
from abc import ABC, abstractmethod


class BaseEffect(ABC):
    """Abstract base class for all effects - demonstrates inheritance and polymorphism"""
    
    @abstractmethod
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """Apply the effect to the image"""
        pass
    
    def validate_params(self, **kwargs):
        """Validate effect parameters - demonstrates encapsulation"""
        pass


class ColorAdjustment(BaseEffect):
    """Base class for color adjustments - demonstrates inheritance"""
    
    def validate_range(self, value: float, min_val: float, max_val: float, param_name: str):
        """Validate parameter range - demonstrates encapsulation"""
        if not min_val <= value <= max_val:
            raise ValueError(f"{param_name} must be between {min_val} and {max_val}")


class BrightnessContrastEffect(ColorAdjustment):
    """Apply brightness and contrast adjustments"""
    
    def apply(self, image: np.ndarray, brightness: int = 0, contrast: float = 1.0) -> np.ndarray:
        self.validate_range(brightness, -100, 100, "Brightness")
        self.validate_range(contrast, 0.1, 3.0, "Contrast")
        
        beta = int(brightness * 2.55)
        return cv2.convertScaleAbs(image, alpha=contrast, beta=beta)


class GammaEffect(ColorAdjustment):
    """Apply gamma correction"""
    
    def apply(self, image: np.ndarray, gamma: float = 1.0) -> np.ndarray:
        self.validate_range(gamma, 0.1, 3.0, "Gamma")
        
        if abs(gamma - 1.0) < 0.001:
            return image
        
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        return cv2.LUT(image, table)


class SaturationEffect(ColorAdjustment):
    """Adjust image saturation"""
    
    def apply(self, image: np.ndarray, saturation: int = 100) -> np.ndarray:
        self.validate_range(saturation, 0, 200, "Saturation")
        
        if saturation == 100:
            return image
        
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = hsv[:, :, 1] * (saturation / 100.0)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)


class BlurEffect(BaseEffect):
    """Apply Gaussian blur"""
    
    def apply(self, image: np.ndarray, kernel_size: int = 0) -> np.ndarray:
        
        if kernel_size <= 0:
            return image
        
        # GaussianBlur requires odd kernel size
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        # Ensure minimum kernel size
        kernel_size = max(3, kernel_size)
        
        # Apply Gaussian blur 
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


class SharpenEffect(BaseEffect):
    """Sharpen image using unsharp mask - KEPT for quick filters"""
    
    def apply(self, image: np.ndarray, amount: float = 0.0) -> np.ndarray:
        self.validate_range(amount, 0.0, 5.0, "Sharpen amount")
        
        if amount <= 0:
            return image
        
        blurred = cv2.GaussianBlur(image, (0, 0), sigmaX=1.5, sigmaY=1.5)
        sharpened = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
        return sharpened


class GrayscaleEffect(BaseEffect):
    """Convert image to grayscale"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


class EdgeDetectionEffect(BaseEffect):
    """Apply Canny edge detection"""
    
    def apply(self, image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


class RotationEffect(BaseEffect):
    """Rotate image by specific angles"""
    
    def apply(self, image: np.ndarray, angle: int = 90) -> np.ndarray:
        if angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        elif angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        elif angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            return cv2.warpAffine(image, M, (w, h))
    
    def validate_params(self, angle: int):
        if angle not in [90, 180, 270]:
            raise ValueError("Angle must be 90, 180, or 270 degrees")


class FlipEffect(BaseEffect):
    """Flip image horizontally or vertically"""
    
    def apply(self, image: np.ndarray, mode: str = "horizontal") -> np.ndarray:
        if mode == "horizontal":
            return cv2.flip(image, 1)
        elif mode == "vertical":
            return cv2.flip(image, 0)
        else:
            raise ValueError("Mode must be 'horizontal' or 'vertical'")


class ResizeEffect(BaseEffect):
    """Resize image to specified dimensions"""
    
    def apply(self, image: np.ndarray, width: int, height: int) -> np.ndarray:
        if width < 1 or height < 1:
            raise ValueError("Width and height must be positive")
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)


class SepiaEffect(BaseEffect):
    """Apply sepia tone filter"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel = np.array([
            [0.131, 0.534, 0.272],
            [0.168, 0.686, 0.349],
            [0.189, 0.769, 0.393],
        ], dtype=np.float32)
        
        sepia = cv2.transform(image, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)


class EmbossEffect(BaseEffect):
    """Apply emboss filter"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel = np.array([
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2],
        ], dtype=np.float32)
        
        return cv2.filter2D(image, -1, kernel)


class SketchEffect(BaseEffect):
    """Apply pencil sketch effect"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        inv = 255 - gray
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        sketch = cv2.divide(gray, 255 - blur, scale=256)
        return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)


class InvertEffect(BaseEffect):
    """Invert colors"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        return 255 - image


class BoundaryExtractionEffect(BaseEffect):
    """Extract boundaries using morphological gradient"""
    
    def apply(self, image: np.ndarray, **kwargs) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(gray, kernel, iterations=1)
        eroded = cv2.erode(gray, kernel, iterations=1)
        gradient = cv2.absdiff(dilated, eroded)
        return cv2.cvtColor(gradient, cv2.COLOR_GRAY2BGR)


class BlackWhiteEffect(BaseEffect):
    """Convert to black and white using thresholding"""
    
    def apply(self, image: np.ndarray, threshold: int = 127) -> np.ndarray:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        return cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)


class EffectsProcessor:
    """
    Main processor class that coordinates all effects.
    Demonstrates class interaction and encapsulation.
    """
    
    def __init__(self):
        """Initialize all effect processors - demonstrates constructor"""
        self.effects = {
            "brightness_contrast": BrightnessContrastEffect(),
            "gamma": GammaEffect(),
            "saturation": SaturationEffect(),
            "sharpen": SharpenEffect(),  # Keep for quick filters
            "blur": BlurEffect(),
            "grayscale": GrayscaleEffect(),
            "edges": EdgeDetectionEffect(),
            "rotation": RotationEffect(),
            "flip": FlipEffect(),
            "resize": ResizeEffect(),
            "sepia": SepiaEffect(),
            "emboss": EmbossEffect(),
            "sketch": SketchEffect(),
            "invert": InvertEffect(),
            "boundary": BoundaryExtractionEffect(),
            "black_white": BlackWhiteEffect(),
        }
    
    def apply_brightness_contrast(self, image: np.ndarray, brightness: int, contrast: float) -> np.ndarray:
        return self.effects["brightness_contrast"].apply(image, brightness=brightness, contrast=contrast)
    
    def apply_gamma(self, image: np.ndarray, gamma: float) -> np.ndarray:
        return self.effects["gamma"].apply(image, gamma=gamma)
    
    def apply_saturation(self, image: np.ndarray, saturation: int) -> np.ndarray:
        return self.effects["saturation"].apply(image, saturation=saturation)
    
    def apply_sharpen(self, image: np.ndarray, amount: float) -> np.ndarray:
        return self.effects["sharpen"].apply(image, amount=amount)
    
    def apply_blur(self, image: np.ndarray, kernel_size: int) -> np.ndarray:
        """Apply blur effect - FIXED TO WORK 100%"""
        return self.effects["blur"].apply(image, kernel_size)
    
    def apply_grayscale(self, image: np.ndarray) -> np.ndarray:
        return self.effects["grayscale"].apply(image)
    
    def apply_edge_detection(self, image: np.ndarray, threshold1: int = 50, threshold2: int = 150) -> np.ndarray:
        return self.effects["edges"].apply(image, threshold1=threshold1, threshold2=threshold2)
    
    def rotate_image(self, image: np.ndarray, angle: int) -> np.ndarray:
        return self.effects["rotation"].apply(image, angle=angle)
    
    def flip_image(self, image: np.ndarray, mode: str) -> np.ndarray:
        return self.effects["flip"].apply(image, mode=mode)
    
    def resize_image(self, image: np.ndarray, width: int, height: int) -> np.ndarray:
        return self.effects["resize"].apply(image, width=width, height=height)
    
    def apply_sepia(self, image: np.ndarray) -> np.ndarray:
        return self.effects["sepia"].apply(image)
    
    def apply_emboss(self, image: np.ndarray) -> np.ndarray:
        return self.effects["emboss"].apply(image)
    
    def apply_sketch(self, image: np.ndarray) -> np.ndarray:
        return self.effects["sketch"].apply(image)
    
    def apply_invert(self, image: np.ndarray) -> np.ndarray:
        return self.effects["invert"].apply(image)
    
    def apply_boundary_extraction(self, image: np.ndarray) -> np.ndarray:
        return self.effects["boundary"].apply(image)
    
    def apply_black_white(self, image: np.ndarray, threshold: int = 127) -> np.ndarray:
        return self.effects["black_white"].apply(image, threshold=threshold)
    
    def render_adjustments(self, base_image: np.ndarray, adjustments: Dict[str, Any]) -> np.ndarray:
        """
        Render multiple adjustments in proper order.
        FIXED: Blur now works 100%.
        
        Args:
            base_image: The base image to apply adjustments to
            adjustments: Dictionary of adjustment values
            
        Returns:
            Processed image with all adjustments applied
        """
        if base_image is None:
            return None
        
        img = base_image.copy()
        
        # Apply adjustments in optimal order:
        # 1. Blur (affects all subsequent operations) 
        blur_val = int(adjustments.get("blur", 0))
        if blur_val > 0:
            img = self.apply_blur(img, blur_val)
        
        # 2. Brightness/Contrast (basic tone adjustment)
        brightness = int(adjustments.get("brightness", 0))
        contrast = float(adjustments.get("contrast", 1.0))
        if brightness != 0 or contrast != 1.0:
            img = self.apply_brightness_contrast(img, brightness, contrast)
        
        # 3. Gamma correction (mid-tone adjustment)
        gamma = float(adjustments.get("gamma", 1.0))
        if abs(gamma - 1.0) > 0.01:
            img = self.apply_gamma(img, gamma)
        
        # 4. Saturation (color intensity)
        saturation = int(adjustments.get("saturation", 100))
        if saturation != 100:
            img = self.apply_saturation(img, saturation)
        
        return img
