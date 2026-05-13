# visual_engine/diff_highlighter.py
# Creates polished, annotated diff images for the HTML report
# Takes raw OpenCV diff output and makes it visually clear
# and professional looking

import os
import cv2
import numpy as np
from utils.config_loader import config


class DiffHighlighter:
    """
    Enhances diff images with annotations and labels.
    Makes visual differences immediately obvious to
    anyone reading the DualGuard report.
    """

    # Colours in BGR format (OpenCV uses BGR not RGB)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (0, 255, 255)
    ORANGE = (0, 165, 255)

    def __init__(self):
        test_config = config.get_test_config()
        self.diff_dir = test_config.get(
            "diff_dir", "reports/diffs"
        )
        os.makedirs(self.diff_dir, exist_ok=True)

    # ──────────────────────────────────────────
    # Main Highlighting Method
    # ──────────────────────────────────────────

    def create_highlighted_diff(
        self,
        english_path: str,
        arabic_path: str,
        screen_name: str,
        similarity_score: float,
        status: str
    ) -> str:
        """
        Creates a fully annotated side-by-side diff image.
        english_path: path to English screenshot
        arabic_path: path to Arabic screenshot
        screen_name: name for the output file
        similarity_score: score from ImageComparator
        status: status string from ImageComparator
        Returns: path to the saved highlighted diff image
        """
        # Load images
        english_img = cv2.imread(english_path)
        arabic_img = cv2.imread(arabic_path)

        # Resize Arabic to match English if needed
        arabic_img = self._resize_to_match(
            arabic_img, english_img
        )

        # Generate diff overlay
        diff_overlay = self._create_diff_overlay(
            english_img, arabic_img
        )

        # Add labels to each panel
        english_labeled = self._add_panel_label(
            english_img.copy(),
            "ENGLISH (LTR)",
            self.GREEN
        )
        arabic_labeled = self._add_panel_label(
            arabic_img.copy(),
            "ARABIC (RTL)",
            self.BLUE
        )
        diff_labeled = self._add_panel_label(
            diff_overlay,
            "VISUAL DIFF",
            self.RED
        )

        # Combine all three panels side by side
        combined = np.hstack([
            english_labeled,
            arabic_labeled,
            diff_labeled
        ])

        # Add header bar with test info
        combined = self._add_header(
            combined,
            screen_name,
            similarity_score,
            status
        )

        # Save final image
        output_path = os.path.join(
            self.diff_dir,
            f"{screen_name}_highlighted.png"
        )
        cv2.imwrite(output_path, combined)
        print(f"Highlighted diff saved: {output_path}")
        return output_path

    # ──────────────────────────────────────────
    # Image Processing Methods
    # ──────────────────────────────────────────

    def _create_diff_overlay(self, img1, img2):
        """
        Creates a diff overlay with differences highlighted in red.
        Areas with differences glow red over the English image.
        """
        # Calculate absolute difference
        diff = cv2.absdiff(img1, img2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # Apply threshold to isolate meaningful differences
        _, thresh = cv2.threshold(
            diff_gray, 30, 255, cv2.THRESH_BINARY
        )

        # Dilate to make differences more visible
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        # Find contours of different regions
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Draw red rectangles around different regions
        overlay = img1.copy()
        for contour in contours:
            if cv2.contourArea(contour) > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(
                    overlay,
                    (x, y),
                    (x + w, y + h),
                    self.RED,
                    2
                )

        return overlay

    def _add_panel_label(
        self, img, label: str, color: tuple
    ):
        """
        Adds a coloured label bar at the top of an image panel.
        label: text to display
        color: BGR colour tuple for the bar
        """
        bar_height = 40
        height, width = img.shape[:2]

        # Create label bar
        bar = np.zeros((bar_height, width, 3), dtype=np.uint8)
        bar[:] = color

        # Add text to bar
        cv2.putText(
            bar,
            label,
            (10, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            self.WHITE,
            2,
            cv2.LINE_AA
        )

        # Stack bar on top of image
        return np.vstack([bar, img])

    def _add_header(
        self,
        img,
        screen_name: str,
        similarity_score: float,
        status: str
    ):
        """
        Adds a header bar at the top of the combined image.
        Shows screen name, similarity score, and status.
        """
        height, width = img.shape[:2]
        header_height = 60

        # Choose header colour based on status
        if "PASS" in status:
            header_color = (0, 120, 0)
        elif "FLAG" in status:
            header_color = (0, 0, 180)
        else:
            header_color = (0, 100, 180)

        # Create header bar
        header = np.zeros(
            (header_height, width, 3), dtype=np.uint8
        )
        header[:] = header_color

        # Add screen name
        cv2.putText(
            header,
            f"Screen: {screen_name.replace('_', ' ').title()}",
            (10, 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.WHITE,
            2,
            cv2.LINE_AA
        )

        # Add similarity score
        cv2.putText(
            header,
            f"Similarity: {similarity_score:.1f}%",
            (10, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            self.WHITE,
            1,
            cv2.LINE_AA
        )

        # Add status on the right side
        status_short = status.split("—")[0].strip()
        text_size = cv2.getTextSize(
            status_short,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            2
        )[0]
        text_x = width - text_size[0] - 20
        cv2.putText(
            header,
            status_short,
            (text_x, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            self.YELLOW,
            2,
            cv2.LINE_AA
        )

        return np.vstack([header, img])

    def _resize_to_match(self, img, reference_img):
        """Resizes img to match reference_img dimensions."""
        ref_height, ref_width = reference_img.shape[:2]
        img_height, img_width = img.shape[:2]

        if img_height != ref_height or img_width != ref_width:
            img = cv2.resize(
                img,
                (ref_width, ref_height),
                interpolation=cv2.INTER_AREA
            )
        return img

    # ──────────────────────────────────────────
    # Batch Processing
    # ──────────────────────────────────────────

    def highlight_all(self, comparison_results: list) -> list:
        """
        Creates highlighted diffs for all comparison results.
        comparison_results: list from ImageComparator.compare_all()
        Returns: list of highlighted diff image paths
        """
        highlighted_paths = []
        for result in comparison_results:
            path = self.create_highlighted_diff(
                english_path=result["english_path"],
                arabic_path=result["arabic_path"],
                screen_name=result["screen_name"],
                similarity_score=result["similarity_score"],
                status=result["status"]
            )
            highlighted_paths.append(path)
        return highlighted_paths