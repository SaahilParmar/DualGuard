# reports/report_generator.py
# Generates DualGuard's signature HTML report
# Shows English and Arabic screenshots side by side
# with visual diff images and comparison scores

import os
import base64
from datetime import datetime
from visual_engine.image_comparator import ImageComparator
from utils.config_loader import config


class ReportGenerator:
    """
    Generates DualGuard's HTML comparison report.
    Creates a professional, visually striking report
    showing English vs Arabic test results side by side.
    """

    def __init__(self):
        self.test_config = config.get_test_config()
        self.screenshot_dir = self.test_config.get(
            "screenshot_dir", "reports/screenshots"
        )
        self.diff_dir = self.test_config.get(
            "diff_dir", "reports/diffs"
        )
        self.report_path = "reports/dualguard_report.html"
        self.comparator = ImageComparator()

    # ──────────────────────────────────────────
    # Main Report Generation
    # ──────────────────────────────────────────

    def generate(self, comparison_results: list) -> str:
        """
        Generates the full HTML report.
        comparison_results: list from ImageComparator
        Returns: path to generated HTML report
        """
        summary = self.comparator.get_summary(
            comparison_results
        )
        html = self._build_html(
            comparison_results, summary
        )
        os.makedirs("reports", exist_ok=True)
        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\nDualGuard report generated: {self.report_path}")
        return self.report_path

    # ──────────────────────────────────────────
    # HTML Building
    # ──────────────────────────────────────────

    def _build_html(
        self, results: list, summary: dict
    ) -> str:
        """Builds the complete HTML report string."""
        timestamp = datetime.now().strftime(
            "%d %B %Y — %H:%M:%S"
        )
        screen_cards = "\n".join([
            self._build_screen_card(r) for r in results
        ])

        return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DualGuard — Bilingual Visual Regression Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont,
                'Segoe UI', Roboto, sans-serif;
            background: #0f0f1a;
            color: #e0e0e0;
            min-height: 100vh;
        }}

        /* Header */
        .header {{
            background: linear-gradient(
                135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%
            );
            padding: 40px;
            text-align: center;
            border-bottom: 2px solid #e94560;
        }}

        .header h1 {{
            font-size: 2.5em;
            color: #ffffff;
            letter-spacing: 3px;
            margin-bottom: 8px;
        }}

        .header h1 span {{
            color: #e94560;
        }}

        .header p {{
            color: #a0a0b0;
            font-size: 1em;
            margin-top: 8px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
            margin: 4px;
        }}

        .badge-blue {{
            background: #0f3460;
            color: #4fc3f7;
            border: 1px solid #4fc3f7;
        }}

        .badge-red {{
            background: #3d0000;
            color: #ef5350;
            border: 1px solid #ef5350;
        }}

        /* Summary Cards */
        .summary {{
            display: grid;
            grid-template-columns: repeat(
                auto-fit, minmax(150px, 1fr)
            );
            gap: 16px;
            padding: 32px 40px;
            background: #12121f;
        }}

        .summary-card {{
            background: #1a1a2e;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid #2a2a4a;
            transition: transform 0.2s;
        }}

        .summary-card:hover {{
            transform: translateY(-4px);
        }}

        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 4px;
        }}

        .summary-card .label {{
            font-size: 0.8em;
            color: #a0a0b0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .number-blue {{ color: #4fc3f7; }}
        .number-green {{ color: #66bb6a; }}
        .number-red {{ color: #ef5350; }}
        .number-yellow {{ color: #ffa726; }}
        .number-purple {{ color: #ab47bc; }}

        /* Overall Status Banner */
        .status-banner {{
            margin: 0 40px 32px;
            padding: 16px 24px;
            border-radius: 12px;
            text-align: center;
            font-size: 1.1em;
            font-weight: bold;
            letter-spacing: 1px;
        }}

        .status-pass {{
            background: #1b3a1b;
            color: #66bb6a;
            border: 1px solid #66bb6a;
        }}

        .status-issues {{
            background: #3d1515;
            color: #ef5350;
            border: 1px solid #ef5350;
        }}

        /* Screen Cards */
        .screens-container {{
            padding: 0 40px 40px;
        }}

        .screens-container h2 {{
            color: #ffffff;
            font-size: 1.3em;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 1px solid #2a2a4a;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .screen-card {{
            background: #1a1a2e;
            border-radius: 16px;
            margin-bottom: 32px;
            overflow: hidden;
            border: 1px solid #2a2a4a;
            transition: box-shadow 0.3s;
        }}

        .screen-card:hover {{
            box-shadow: 0 8px 32px rgba(233, 69, 96, 0.2);
        }}

        .card-header {{
            padding: 20px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #12121f;
            border-bottom: 1px solid #2a2a4a;
        }}

        .card-header h3 {{
            color: #ffffff;
            font-size: 1.1em;
            text-transform: capitalize;
        }}

        .score {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .score-bar-container {{
            width: 120px;
            height: 8px;
            background: #2a2a4a;
            border-radius: 4px;
            overflow: hidden;
        }}

        .score-bar {{
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease;
        }}

        .score-text {{
            font-size: 0.9em;
            font-weight: bold;
            min-width: 48px;
        }}

        .status-pill {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
        }}

        .pill-pass {{
            background: #1b3a1b;
            color: #66bb6a;
        }}

        .pill-flag {{
            background: #3d1515;
            color: #ef5350;
        }}

        .pill-similar {{
            background: #1a2a3d;
            color: #ffa726;
        }}

        /* Image Grid */
        .image-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 2fr;
            gap: 1px;
            background: #2a2a4a;
        }}

        .image-panel {{
            background: #1a1a2e;
            padding: 16px;
        }}

        .image-panel h4 {{
            color: #a0a0b0;
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
            text-align: center;
        }}

        .image-panel h4.english-label {{
            color: #66bb6a;
        }}

        .image-panel h4.arabic-label {{
            color: #4fc3f7;
        }}

        .image-panel h4.diff-label {{
            color: #ef5350;
        }}

        .image-panel img {{
            width: 100%;
            border-radius: 8px;
            border: 1px solid #2a2a4a;
        }}

        /* Meta Info */
        .card-meta {{
            padding: 12px 24px;
            display: flex;
            gap: 24px;
            background: #12121f;
            border-top: 1px solid #2a2a4a;
            font-size: 0.8em;
            color: #a0a0b0;
        }}

        .meta-item span {{
            color: #ffffff;
            font-weight: bold;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 32px;
            color: #606070;
            font-size: 0.85em;
            border-top: 1px solid #2a2a4a;
        }}

        .footer strong {{
            color: #e94560;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .image-grid {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{ font-size: 1.8em; }}
            .summary {{ padding: 20px; }}
            .screens-container {{ padding: 0 20px 20px; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <div class="header">
        <h1>DUAL<span>GUARD</span></h1>
        <p>Bilingual Arabic / English Visual Regression Report</p>
        <p style="margin-top: 12px;">
            <span class="badge badge-blue">
                🕐 {timestamp}
            </span>
            <span class="badge badge-blue">
                📱 Wikipedia Android App
            </span>
            <span class="badge badge-red">
                🌐 Arabic RTL + English LTR
            </span>
        </p>
    </div>

    <!-- Summary Cards -->
    <div class="summary">
        <div class="summary-card">
            <div class="number number-blue">
                {summary["total_comparisons"]}
            </div>
            <div class="label">Screens Tested</div>
        </div>
        <div class="summary-card">
            <div class="number number-green">
                {summary["passed"]}
            </div>
            <div class="label">Passed</div>
        </div>
        <div class="summary-card">
            <div class="number number-red">
                {summary["flagged"]}
            </div>
            <div class="label">Flagged</div>
        </div>
        <div class="summary-card">
            <div class="number number-purple">
                {summary["rtl_detected"]}
            </div>
            <div class="label">RTL Detected</div>
        </div>
        <div class="summary-card">
            <div class="number number-yellow">
                {summary["pass_rate"]}%
            </div>
            <div class="label">Pass Rate</div>
        </div>
    </div>

    <!-- Status Banner -->
    <div class="status-banner {
        'status-pass'
        if summary['overall_status'] == 'PASS'
        else 'status-issues'
    }">
        Overall Status: {summary["overall_status"]}
    </div>

    <!-- Screen Cards -->
    <div class="screens-container">
        <h2>📱 Screen Comparisons</h2>
        {screen_cards}
    </div>

    <!-- Footer -->
    <div class="footer">
        Generated by <strong>DualGuard</strong> —
        Built by Saahil Parmar |
        github.com/SaahilParmar/DualGuard
    </div>

</body>
</html>"""

    def _build_screen_card(self, result: dict) -> str:
        """Builds a single screen comparison card."""
        screen_name = result["screen_name"].replace(
            "_", " "
        ).title()
        score = result["similarity_score"]
        status = result["status"]

        # Score bar colour
        if score >= 70:
            bar_color = "#ffa726"
        elif score >= 40:
            bar_color = "#66bb6a"
        else:
            bar_color = "#ef5350"

        # Status pill class
        if "PASS" in status:
            pill_class = "pill-pass"
        elif "FLAG" in status:
            pill_class = "pill-flag"
        else:
            pill_class = "pill-similar"

        # Encode images as base64 for self-contained HTML
        english_b64 = self._encode_image(
            result["english_path"]
        )
        arabic_b64 = self._encode_image(
            result["arabic_path"]
        )
        diff_b64 = self._encode_image(
            result["diff_path"]
        )

        rtl_text = (
            "✅ RTL Detected"
            if result["is_rtl_detected"]
            else "⚠️ RTL Not Detected"
        )
        dim_text = (
            "✅ Match"
            if result["dimensions_match"]
            else "⚠️ Mismatch"
        )

        return f"""
        <div class="screen-card">
            <div class="card-header">
                <h3>📱 {screen_name}</h3>
                <div class="score">
                    <div class="score-bar-container">
                        <div class="score-bar" style="
                            width: {score}%;
                            background: {bar_color};
                        "></div>
                    </div>
                    <span class="score-text" style="
                        color: {bar_color};
                    ">{score}%</span>
                    <span class="status-pill {pill_class}">
                        {status.split("—")[0].strip()}
                    </span>
                </div>
            </div>
            <div class="image-grid">
                <div class="image-panel">
                    <h4 class="english-label">
                        🇬🇧 English (LTR)
                    </h4>
                    <img src="data:image/png;base64,{english_b64}"
                         alt="English {screen_name}">
                </div>
                <div class="image-panel">
                    <h4 class="arabic-label">
                        🇦🇪 Arabic (RTL)
                    </h4>
                    <img src="data:image/png;base64,{arabic_b64}"
                         alt="Arabic {screen_name}">
                </div>
                <div class="image-panel">
                    <h4 class="diff-label">
                        🔍 Visual Diff
                    </h4>
                    <img src="data:image/png;base64,{diff_b64}"
                         alt="Diff {screen_name}">
                </div>
            </div>
            <div class="card-meta">
                <div class="meta-item">
                    Layout: <span>{rtl_text}</span>
                </div>
                <div class="meta-item">
                    Dimensions: <span>{dim_text}</span>
                </div>
                <div class="meta-item">
                    Similarity: <span>{score}%</span>
                </div>
                <div class="meta-item">
                    Threshold: <span>{result["threshold"]}%</span>
                </div>
            </div>
        </div>"""

    # ──────────────────────────────────────────
    # Image Encoding
    # ──────────────────────────────────────────

    def _encode_image(self, image_path: str) -> str:
        """
        Encodes an image as base64 string.
        This embeds images directly into the HTML file
        so the report is fully self-contained.
        """
        if not image_path or not os.path.exists(image_path):
            # Return a small transparent placeholder
            return (
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
                "CAQAAABnepAAAAC0lEQVR42mNkYAAAAAY"
                "AAjCB0C8AAAAASUVORK5CYII="
            )
        with open(image_path, "rb") as img_file:
            return base64.b64encode(
                img_file.read()
            ).decode("utf-8")