#!/usr/bin/env python3
"""
Generate a fillable (interactive) PDF for the Mise Onboarding Form.
Uses reportlab with AcroForm fields so recipients can type directly into the PDF.
Branded with Mise colors, logo, and fonts.
"""

import base64
import shutil
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

# Mise brand colors
NAVY = HexColor('#1B2A4E')
RED = HexColor('#B5402F')
CREAM = HexColor('#F9F6F1')
LIGHT_GRAY = HexColor('#E8E8E8')
WHITE = white

# Paths
LOGO_PATH = Path.home() / "mise-core/Branding/Logo Files/Updated Mise Logo Pronunciation.png"
ICON_PATH = Path.home() / "mise-core/Branding/Logo Files/Icon No Background.png"
FONT_DIR = Path.home() / "mise-core/Branding/fonts/Inter"
OUTPUT_DIR = Path.home() / "mise-core/fundraising"
GDRIVE_LIBRARY = Path.home() / "Library/CloudStorage/GoogleDrive-jonathan@papasurf.com/My Drive/Mise/docs/mise_library"

# Register Inter font family
pdfmetrics.registerFont(TTFont('Inter', str(FONT_DIR / 'Inter-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Inter-Bold', str(FONT_DIR / 'Inter-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Inter-Italic', str(FONT_DIR / 'Inter-Italic.ttf')))
pdfmetrics.registerFont(TTFont('Inter-BoldItalic', str(FONT_DIR / 'Inter-BoldItalic.ttf')))
pdfmetrics.registerFontFamily('Inter', normal='Inter', bold='Inter-Bold',
                              italic='Inter-Italic', boldItalic='Inter-BoldItalic')

# Page setup
PAGE_W, PAGE_H = letter  # 612 x 792
MARGIN = 0.75 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

# Field counter for unique names
field_counter = [0]

def next_field_name(prefix="field"):
    field_counter[0] += 1
    return f"{prefix}_{field_counter[0]}"


def draw_text_field(c, x, y, width, height=18, name=None):
    """Draw an editable text field."""
    if name is None:
        name = next_field_name("text")
    c.acroForm.textfield(
        name=name,
        x=x, y=y,
        width=width, height=height,
        borderWidth=1,
        borderColor=LIGHT_GRAY,
        fillColor=HexColor('#FAFAFA'),
        textColor=NAVY,
        fontSize=10,
        fieldFlags='',
    )


def draw_checkbox(c, x, y, name=None, size=12):
    """Draw a checkbox field."""
    if name is None:
        name = next_field_name("cb")
    c.acroForm.checkbox(
        name=name,
        x=x, y=y + 2,
        size=size,
        borderWidth=1,
        borderColor=RED,
        fillColor=HexColor('#FAFAFA'),
        buttonStyle='check',
        checked=False,
    )


def draw_multiline_field(c, x, y, width, height=50, name=None):
    """Draw a multiline text field."""
    if name is None:
        name = next_field_name("multi")
    c.acroForm.textfield(
        name=name,
        x=x, y=y,
        width=width, height=height,
        borderWidth=1,
        borderColor=LIGHT_GRAY,
        fillColor=HexColor('#FAFAFA'),
        textColor=NAVY,
        fontSize=10,
        fieldFlags='multiline',
    )


class MiseFormBuilder:
    def __init__(self, filename):
        self.filename = filename
        self.c = canvas.Canvas(str(filename), pagesize=letter)
        self.y = PAGE_H - MARGIN  # Current y position (top-down)
        self.page_num = 0

    def new_page(self, accent=False):
        """Start a new page. If accent=True, draws top accent strip."""
        if self.page_num > 0:
            # Page number footer
            self.c.setFont("Inter", 9)
            self.c.setFillColor(NAVY)
            self.c.drawCentredString(PAGE_W / 2, 0.4 * inch, str(self.page_num))
            self.c.showPage()
        self.page_num += 1
        self.y = PAGE_H - MARGIN
        if accent:
            self.draw_page_top_accent()

    def check_space(self, needed):
        """Check if we need a new page. Inner pages get the accent strip."""
        if self.y - needed < MARGIN + 30:
            self.new_page(accent=(self.page_num > 1))
            return True
        return False

    def draw_page1(self):
        """Draw the complete branded page 1 (cover/hero + Section 1)."""
        self.new_page()

        # ── LOGO AREA ──
        logo_bottom = PAGE_H - MARGIN
        if LOGO_PATH.exists():
            img = ImageReader(str(LOGO_PATH))
            iw, ih = img.getSize()
            logo_width = 130
            logo_height = logo_width * (ih / iw)
            logo_x = MARGIN + 10
            logo_y = PAGE_H - MARGIN - logo_height + 5
            logo_bottom = logo_y - 12
            # Navy accent line flush left of logo
            self.c.setStrokeColor(NAVY)
            self.c.setLineWidth(3)
            self.c.line(MARGIN, PAGE_H - MARGIN + 5, MARGIN, logo_y)
            self.c.drawImage(img, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')

        # ── NAVY HERO BANNER (full bleed) ──
        banner_top = logo_bottom - 8
        banner_height = 100
        banner_bottom = banner_top - banner_height
        self.c.setFillColor(NAVY)
        self.c.rect(0, banner_bottom, PAGE_W, banner_height, fill=1, stroke=0)
        # Red accent line at bottom edge
        self.c.setStrokeColor(RED)
        self.c.setLineWidth(3)
        self.c.line(0, banner_bottom, PAGE_W, banner_bottom)

        # Title (white on navy)
        self.c.setFont("Inter-Bold", 28)
        self.c.setFillColor(WHITE)
        self.c.drawString(MARGIN + 4, banner_bottom + 52, "New Client Onboarding Form")
        # Subtitle (muted on navy)
        self.c.setFont("Inter", 13)
        self.c.setFillColor(HexColor('#B8C4D8'))
        self.c.drawString(MARGIN + 4, banner_bottom + 28, "Everything Mise needs to get you running.")

        self.y = banner_bottom - 20

        # ── CALLOUT ──
        self.draw_callout(
            "This should take about 10 minutes.",
            "Fill out what you can. If you're unsure about anything, leave it blank and we'll figure it out together during setup.\n"
            "The fastest way to handle Section 2 is to pull your Employee List export from Toast and send it to jon@getmise.io.",
            "tip"
        )

        self.y -= 6

        # ── SECTION 1: CREAM CARD ──
        main_fields = [
            ("Business Name", None, "restaurant_name"),
            ("Address", None, "location"),
            ("Days Open", "e.g., Mon–Sun, Tue–Sat", "days_open"),
            ("Contact Full Name", None, "contact_name"),
            ("Contact Phone", None, "contact_phone"),
            ("Contact Email", None, "contact_email"),
        ]
        label_font_size = 11
        field_row_h = 32
        hint_h = 16

        # Card height: header(34) + main fields + pay period inner card(72) + padding
        card_height = 34
        for _, hint, _ in main_fields:
            card_height += field_row_h + (hint_h if hint else 0)
        pay_inner_h = 72  # inner card for pay period
        card_height += 12 + pay_inner_h + 16  # gap + inner card + bottom padding

        card_x = MARGIN - 8
        card_w = CONTENT_W + 16
        card_top = self.y + 16
        card_bottom = card_top - card_height

        # Draw cream card background
        self.c.setFillColor(CREAM)
        self.c.setStrokeColor(HexColor('#DDD8D0'))
        self.c.setLineWidth(0.5)
        self.c.roundRect(card_x, card_bottom, card_w, card_height, 6, fill=1, stroke=1)
        # Navy left accent bar on card
        self.c.setFillColor(NAVY)
        self.c.rect(card_x, card_bottom, 4, card_height, fill=1, stroke=0)

        # Section header
        self.y -= 6
        self.c.setFont("Inter-Bold", 15)
        self.c.setFillColor(RED)
        self.c.drawString(MARGIN + 4, self.y, "Section 1: About Your Business")
        self.y -= 6
        self.c.setStrokeColor(HexColor('#D4CFC7'))
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN + 4, self.y, PAGE_W - MARGIN - 4, self.y)
        self.y -= 22

        # Main fields
        for label, hint, name in main_fields:
            self.c.setFont("Inter-Bold", label_font_size)
            self.c.setFillColor(NAVY)
            self.c.drawString(MARGIN + 4, self.y, label)
            field_x = MARGIN + 170
            field_w = CONTENT_W - 170
            draw_text_field(self.c, field_x, self.y - 4, field_w, name=name)
            if hint:
                self.y -= hint_h
                self.c.setFont("Inter-Italic", 8)
                self.c.setFillColor(HexColor('#888888'))
                self.c.drawString(field_x, self.y, hint)
            self.y -= field_row_h

        # ── Pay Period inner card ──
        self.y -= 4
        inner_x = MARGIN + 2
        inner_w = CONTENT_W - 4
        inner_top = self.y + 8
        inner_bottom = inner_top - pay_inner_h

        # White inner card background with subtle border
        self.c.setFillColor(WHITE)
        self.c.setStrokeColor(HexColor('#D4CFC7'))
        self.c.setLineWidth(0.5)
        self.c.roundRect(inner_x, inner_bottom, inner_w, pay_inner_h, 4, fill=1, stroke=1)
        # Red left accent bar on inner card
        self.c.setFillColor(RED)
        self.c.rect(inner_x, inner_bottom, 3, pay_inner_h, fill=1, stroke=0)

        # Pay period sub-header with audiowave icon
        sub_y = inner_top - 18
        icon_size = 11
        if ICON_PATH.exists():
            self.c.drawImage(str(ICON_PATH), inner_x + 10, sub_y - 1,
                             width=icon_size, height=icon_size, mask='auto')
        self.c.setFont("Inter-Bold", 11)
        self.c.setFillColor(NAVY)
        self.c.drawString(inner_x + 10 + icon_size + 5, sub_y, "Pay Period")

        # Start and End side by side
        row_y = sub_y - 28
        half_w = (inner_w - 30) / 2

        # Starts
        self.c.setFont("Inter-Bold", 10)
        self.c.setFillColor(NAVY)
        self.c.drawString(inner_x + 12, row_y, "Starts:")
        draw_text_field(self.c, inner_x + 60, row_y - 4, half_w - 52, name="pay_start")
        self.c.setFont("Inter-Italic", 7)
        self.c.setFillColor(HexColor('#888888'))
        self.c.drawString(inner_x + 60, row_y - 16, "e.g. Monday")

        # Ends
        end_x = inner_x + 12 + half_w + 6
        self.c.setFont("Inter-Bold", 10)
        self.c.setFillColor(NAVY)
        self.c.drawString(end_x, row_y, "Ends:")
        draw_text_field(self.c, end_x + 42, row_y - 4, half_w - 44, name="pay_end")
        self.c.setFont("Inter-Italic", 7)
        self.c.setFillColor(HexColor('#888888'))
        self.c.drawString(end_x + 42, row_y - 16, "e.g. Sunday")

        self.y = card_bottom - 8

    def draw_page_top_accent(self):
        """Draw a thin navy + red accent strip at the top of inner pages."""
        self.c.setFillColor(NAVY)
        self.c.rect(0, PAGE_H - 6, PAGE_W, 6, fill=1, stroke=0)
        self.c.setStrokeColor(RED)
        self.c.setLineWidth(2)
        self.c.line(0, PAGE_H - 7, PAGE_W, PAGE_H - 7)
        self.y = PAGE_H - MARGIN - 4

    def draw_section_header(self, text):
        """Draw a section header (h2 style) with audiowave icon."""
        self.check_space(40)
        self.y -= 10
        # Audiowave icon as bullet
        icon_size = 14
        if ICON_PATH.exists():
            self.c.drawImage(str(ICON_PATH), MARGIN, self.y - 2,
                             width=icon_size, height=icon_size, mask='auto')
        # Section title
        self.c.setFont("Inter-Bold", 14)
        self.c.setFillColor(RED)
        self.c.drawString(MARGIN + icon_size + 6, self.y, text)
        self.y -= 5
        # Subtle underline
        self.c.setStrokeColor(HexColor('#D4CFC7'))
        self.c.setLineWidth(1)
        self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
        self.y -= 16

    def draw_subsection(self, text):
        """Draw subsection header (h3 style) with navy dash."""
        self.check_space(30)
        self.y -= 4
        # Small navy dash accent
        self.c.setStrokeColor(NAVY)
        self.c.setLineWidth(2)
        self.c.line(MARGIN, self.y + 4, MARGIN + 10, self.y + 4)
        self.c.setFont("Inter-Bold", 11)
        self.c.setFillColor(NAVY)
        self.c.drawString(MARGIN + 16, self.y, text)
        self.y -= 16

    def draw_label(self, text, x=None):
        """Draw a field label."""
        if x is None:
            x = MARGIN
        self.c.setFont("Inter-Bold", 10)
        self.c.setFillColor(NAVY)
        self.c.drawString(x, self.y, text)

    def draw_hint(self, text, x=None):
        """Draw hint text (smaller, lighter)."""
        if x is None:
            x = MARGIN
        self.c.setFont("Inter-Italic", 8)
        self.c.setFillColor(HexColor('#888888'))
        self.c.drawString(x, self.y, text)

    def draw_body(self, text, x=None):
        """Draw body text."""
        if x is None:
            x = MARGIN
        self.c.setFont("Inter", 10)
        self.c.setFillColor(NAVY)
        self.c.drawString(x, self.y, text)

    def draw_labeled_field(self, label, field_width=None, hint=None, name=None):
        """Draw a label + text field on the same line."""
        self.check_space(30)
        if field_width is None:
            field_width = CONTENT_W - 180
        self.draw_label(label)
        field_x = MARGIN + 180
        draw_text_field(self.c, field_x, self.y - 4, field_width, name=name)
        if hint:
            self.y -= 16
            self.draw_hint(hint, field_x)
        self.y -= 22

    def draw_callout(self, title, body, style="tip"):
        """Draw a callout box. Body can contain \\n for explicit line breaks."""
        self.check_space(60)
        colors = {
            "tip": (HexColor('#E6F4EA'), HexColor('#2E7D32')),
            "note": (HexColor('#E8EBF0'), NAVY),
            "important": (HexColor('#FDEAEA'), RED),
        }
        bg_color, border_color = colors.get(style, colors["note"])

        # Word wrap body text, respecting explicit \n line breaks
        max_width = CONTENT_W - 30
        all_lines = []
        for paragraph in body.split("\n"):
            words = paragraph.split()
            current = ""
            for w in words:
                test = current + " " + w if current else w
                if pdfmetrics.stringWidth(test, "Inter", 9) < max_width:
                    current = test
                else:
                    all_lines.append(current)
                    current = w
            if current:
                all_lines.append(current)

        box_height = 24 + len(all_lines) * 12 + 6
        # Background
        self.c.setFillColor(bg_color)
        self.c.setStrokeColor(border_color)
        self.c.setLineWidth(0)
        self.c.rect(MARGIN, self.y - box_height + 10, CONTENT_W, box_height, fill=1, stroke=0)
        # Left border
        self.c.setStrokeColor(border_color)
        self.c.setLineWidth(3)
        self.c.line(MARGIN, self.y - box_height + 10, MARGIN, self.y + 10)
        # Title
        self.c.setFont("Inter-Bold", 10)
        self.c.setFillColor(border_color)
        self.c.drawString(MARGIN + 12, self.y, title)
        # Body
        self.c.setFont("Inter", 9)
        self.c.setFillColor(NAVY)
        text_y = self.y - 14
        for line in all_lines:
            self.c.drawString(MARGIN + 12, text_y, line)
            text_y -= 12

        self.y -= box_height + 8

    def draw_table_header(self, cols, col_widths):
        """Draw a table header row."""
        self.check_space(25)
        x = MARGIN
        row_h = 20
        # Header background
        self.c.setFillColor(NAVY)
        self.c.rect(x, self.y - row_h + 6, CONTENT_W, row_h, fill=1, stroke=0)
        # Header text
        self.c.setFont("Inter-Bold", 9)
        self.c.setFillColor(WHITE)
        for i, col in enumerate(cols):
            self.c.drawString(x + 4, self.y - 8, col)
            x += col_widths[i]
        self.y -= row_h

    def draw_table_field_row(self, col_widths, row_num, field_prefix="row"):
        """Draw a table row with fillable fields."""
        self.check_space(24)
        x = MARGIN
        row_h = 22
        # Alternating background
        if row_num % 2 == 0:
            self.c.setFillColor(CREAM)
            self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)

        for i, w in enumerate(col_widths):
            draw_text_field(self.c, x + 2, self.y - row_h + 10, w - 6, height=16,
                           name=next_field_name(f"{field_prefix}_c{i}"))
            x += w
        self.y -= row_h

    def draw_hr(self):
        """Draw a horizontal rule."""
        self.y -= 6
        self.c.setStrokeColor(CREAM)
        self.c.setLineWidth(2)
        self.c.line(MARGIN, self.y, PAGE_W - MARGIN, self.y)
        self.y -= 10

    def draw_pull_quote(self, text, attribution):
        """Draw a centered pull quote."""
        self.check_space(70)
        self.y -= 10
        # Top border
        self.c.setStrokeColor(RED)
        self.c.setLineWidth(2)
        self.c.line(MARGIN + 40, self.y, PAGE_W - MARGIN - 40, self.y)
        self.y -= 24
        # Quote text
        self.c.setFont("Inter-Italic", 14)
        self.c.setFillColor(NAVY)
        self.c.drawCentredString(PAGE_W / 2, self.y, text)
        self.y -= 18
        # Attribution
        self.c.setFont("Inter", 10)
        self.c.setFillColor(RED)
        self.c.drawCentredString(PAGE_W / 2, self.y, attribution)
        self.y -= 10
        # Bottom border
        self.c.setStrokeColor(RED)
        self.c.line(MARGIN + 40, self.y, PAGE_W - MARGIN - 40, self.y)
        self.y -= 16

    def draw_footer(self):
        """Draw Mise tagline footer."""
        self.c.setFont("Inter-Italic", 9)
        self.c.setFillColor(NAVY)
        self.c.drawCentredString(PAGE_W / 2, MARGIN - 10, "Mise: Everything in its place.")

    def build(self):
        """Build the complete form."""

        # ── PAGE 1 ──────────────────────────────────────
        self.draw_page1()

        # ── PAGE 2 ──────────────────────────────────────
        self.new_page(accent=True)

        # Section 2: Team
        self.draw_section_header("Section 2: Your Team")
        self.draw_body("Mise uses voice recordings to process payroll. We need your team's names so we can")
        self.y -= 14
        self.draw_body("accurately recognize them from audio. Include everyone who works tipped shifts.")
        self.y -= 22

        self.draw_callout(
            "Easiest option",
            "Export your Employee List from Toast and email it to jon@getmise.io. That gives us names and IDs instantly. Then just add nicknames below.",
            "note"
        )

        # Servers table
        self.draw_subsection("Servers")
        server_cols = ["#", "Full Name", "Nickname", "Toast Employee ID"]
        server_widths = [25, 200, 130, 145]
        self.draw_table_header(server_cols, server_widths)
        for i in range(10):
            self.check_space(24)
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            # Row number
            self.c.setFont("Inter", 9)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, str(i + 1))
            x += server_widths[0]
            # Fields
            for j in range(1, 4):
                draw_text_field(self.c, x + 2, self.y - row_h + 10, server_widths[j] - 6, height=16,
                               name=f"server_{i+1}_{server_cols[j].lower().replace(' ', '_')}")
                x += server_widths[j]
            self.y -= row_h

        # ── Tipout Calculation Method ──
        self.draw_subsection("How Do You Calculate Tipouts?")
        self.draw_body("What metric do you use to calculate tipouts for support staff?")
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tipout_total_sales")
        self.draw_body("% of total sales", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tipout_food_sales")
        self.draw_body("% of food sales", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tipout_other_metric")
        self.draw_body("% of other metric  \u2014  What metric?", MARGIN + 18)
        draw_text_field(self.c, MARGIN + 230, self.y - 4, CONTENT_W - 230, name="tipout_other_metric_desc")
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tipout_method_other")
        self.draw_body("Other  \u2014  Explain:", MARGIN + 18)
        draw_text_field(self.c, MARGIN + 130, self.y - 4, CONTENT_W - 130, name="tipout_method_other_desc")
        self.y -= 24

        # Support Staff
        self.draw_subsection("Support Staff")

        # Custom support role names
        self.draw_body("What do you call your support roles?")
        self.y -= 14
        self.draw_hint("e.g., Busser, Expo, Runner, Barback, Utility, Food Runner, etc.")
        self.y -= 16
        for i in range(1, 6):
            self.draw_label(f"Role {i}:", MARGIN)
            draw_text_field(self.c, MARGIN + 50, self.y - 4, 140, name=f"support_role_{i}_name")
            self.draw_label("Tipout %:", MARGIN + 210)
            draw_text_field(self.c, MARGIN + 275, self.y - 4, 60, name=f"support_role_{i}_tipout_pct")
            self.y -= 22
        # ── PAGE 3 ──────────────────────────────────────
        self.new_page(accent=True)

        self.draw_subsection("Support Staff (continued)")
        support_cols = ["#", "Full Name", "Nickname", "Toast ID", "Typical Role(s)"]
        support_widths = [25, 150, 100, 80, 145]
        self.draw_table_header(support_cols, support_widths)
        for i in range(8):
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            self.c.setFont("Inter", 9)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, str(i + 1))
            x += support_widths[0]
            for j in range(1, 5):
                draw_text_field(self.c, x + 2, self.y - row_h + 10, support_widths[j] - 6, height=16,
                               name=f"support_{i+1}_{support_cols[j].lower().replace(' ', '_')}")
                x += support_widths[j]
            self.y -= row_h

        self.y -= 8

        # Kitchen staff
        self.draw_subsection("Kitchen Staff Who Receive Tips (if any)")
        kitchen_cols = ["#", "Full Name", "Nickname", "Toast ID"]
        kitchen_widths = [25, 200, 130, 145]
        self.draw_table_header(kitchen_cols, kitchen_widths)
        for i in range(5):
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            self.c.setFont("Inter", 9)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, str(i + 1))
            x += kitchen_widths[0]
            for j in range(1, 4):
                draw_text_field(self.c, x + 2, self.y - row_h + 10, kitchen_widths[j] - 6, height=16,
                               name=f"kitchen_{i+1}_{kitchen_cols[j].lower().replace(' ', '_')}")
                x += kitchen_widths[j]
            self.y -= row_h

        self.y -= 8

        # Who records payroll
        self.draw_subsection("Who Will Record Payroll?")
        rec_cols = ["#", "Full Name", "Role (owner, GM, manager)"]
        rec_widths = [25, 237, 238]
        self.draw_table_header(rec_cols, rec_widths)
        for i in range(3):
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            self.c.setFont("Inter", 9)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, str(i + 1))
            x += rec_widths[0]
            draw_text_field(self.c, x + 2, self.y - row_h + 10, rec_widths[1] - 6, height=16,
                           name=f"recorder_{i+1}_name")
            x += rec_widths[1]
            draw_text_field(self.c, x + 2, self.y - row_h + 10, rec_widths[2] - 6, height=16,
                           name=f"recorder_{i+1}_role")
            self.y -= row_h

        # ── PAGE 4 ──────────────────────────────────────
        self.new_page(accent=True)

        # Section 3: Shifts
        self.draw_section_header("Section 3: Your Shifts")

        # AM/PM table
        shift_cols = ["Shift", "Start Time", "End Time"]
        shift_widths = [120, 190, 190]
        self.draw_table_header(shift_cols, shift_widths)
        for i, shift in enumerate(["AM", "PM"]):
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            self.c.setFont("Inter-Bold", 10)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, shift)
            x += shift_widths[0]
            draw_text_field(self.c, x + 2, self.y - row_h + 10, shift_widths[1] - 6, height=16,
                           name=f"shift_{shift.lower()}_start")
            x += shift_widths[1]
            draw_text_field(self.c, x + 2, self.y - row_h + 10, shift_widths[2] - 6, height=16,
                           name=f"shift_{shift.lower()}_end")
            self.y -= row_h

        self.y -= 12

        # Variable close times
        self.draw_body("Does your PM closing time change by day of the week?")
        self.y -= 25
        draw_checkbox(self.c, MARGIN, self.y, name="close_same")
        self.draw_body("No, same every day", MARGIN + 18)
        self.y -= 27
        draw_checkbox(self.c, MARGIN, self.y, name="close_varies")
        self.draw_body("Yes  \u2014  fill out below:", MARGIN + 18)
        self.y -= 20

        # Day-by-day close times
        day_cols = ["Day", "PM Close Time"]
        day_widths = [120, 380]
        self.draw_table_header(day_cols, day_widths)
        for i, day in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
            x = MARGIN
            row_h = 22
            if i % 2 == 0:
                self.c.setFillColor(CREAM)
                self.c.rect(x, self.y - row_h + 8, CONTENT_W, row_h, fill=1, stroke=0)
            self.c.setFont("Inter", 10)
            self.c.setFillColor(NAVY)
            self.c.drawString(x + 6, self.y - 6, day)
            x += day_widths[0]
            draw_text_field(self.c, x + 2, self.y - row_h + 10, day_widths[1] - 6, height=16,
                           name=f"close_{day.lower()}")
            self.y -= row_h

        self.draw_hr()

        # Section 4: Tip Rules
        self.draw_section_header("Section 4: Tip Rules")

        # Tip pooling
        self.draw_subsection("Tip Pooling")
        self.draw_body("When 2 or more servers work the same shift, what happens to their tips?")
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tip_pool")
        self.draw_body("Pool  \u2014  Tips are combined and split evenly between servers", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tip_individual")
        self.draw_body("Individual  \u2014  Each server keeps their own tips", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="tip_other")
        self.draw_body("Other  \u2014  Explain:", MARGIN + 18)
        draw_text_field(self.c, MARGIN + 115, self.y - 4, CONTENT_W - 115, name="tip_other_desc")
        self.y -= 24

        # Unequal hours — servers
        self.draw_subsection("Unequal Hours in Tip Pool")
        self.draw_body("If a server gets cut early or works fewer hours, how do you handle their share of the pool?")
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="pool_equal_split")
        self.draw_body("Even split regardless of hours worked", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="pool_pro_rate")
        self.draw_body("Pro-rate by hours worked", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="pool_hours_other")
        self.draw_body("Other  \u2014  Explain:", MARGIN + 18)
        draw_text_field(self.c, MARGIN + 115, self.y - 4, CONTENT_W - 115, name="pool_hours_other_desc")
        self.y -= 24

        # Unequal hours — support staff
        self.draw_subsection("Support Staff Tipout \u2014 Unequal Hours")
        self.draw_body("If a support staff member gets cut early, how do you adjust their tipout?")
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="support_tipout_full")
        self.draw_body("Full tipout regardless of hours worked", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="support_tipout_pro_rate")
        self.draw_body("Pro-rate by hours worked", MARGIN + 18)
        self.y -= 18
        draw_checkbox(self.c, MARGIN, self.y, name="support_tipout_hours_other")
        self.draw_body("Other  \u2014  Explain:", MARGIN + 18)
        draw_text_field(self.c, MARGIN + 115, self.y - 4, CONTENT_W - 115, name="support_tipout_hours_other_desc")
        self.y -= 24

        # Free-text for anything else
        self.draw_subsection("Anything Else About Tips?")
        self.draw_hint("Describe any special rules, exceptions, or 'the way we've always done it' here.")
        self.y -= 6
        draw_multiline_field(self.c, MARGIN, self.y - 75, CONTENT_W, height=81, name="tip_notes")
        self.y -= 95

        # ── FINAL PAGE ──────────────────────────────────
        self.new_page()

        # ── Navy top banner (bookend to page 1) ──
        banner_height = 60
        banner_bottom = PAGE_H - banner_height
        self.c.setFillColor(NAVY)
        self.c.rect(0, banner_bottom, PAGE_W, banner_height, fill=1, stroke=0)
        self.c.setStrokeColor(RED)
        self.c.setLineWidth(3)
        self.c.line(0, banner_bottom, PAGE_W, banner_bottom)
        # Title in white
        self.c.setFont("Inter-Bold", 22)
        self.c.setFillColor(WHITE)
        self.c.drawString(MARGIN + 4, banner_bottom + 22, "What Happens Next")

        self.y = banner_bottom - 28

        # ── Numbered steps with red numbers ──
        steps = [
            "We configure Mise for your restaurant",
            "We schedule your setup session \u2014 we come to you, in person",
            "You record your first real payroll with us right there",
            "We make sure everything is right before you go live",
            "You get a direct line to support \u2014 call or text anytime",
        ]
        for i, step in enumerate(steps, 1):
            self.c.setFont("Inter-Bold", 12)
            self.c.setFillColor(RED)
            self.c.drawString(MARGIN + 8, self.y, f"{i}.")
            self.c.setFont("Inter", 11)
            self.c.setFillColor(NAVY)
            self.c.drawString(MARGIN + 30, self.y, step)
            self.y -= 22

        # ── Centered statement ──
        self.y -= 16
        self.c.setFont("Inter-Bold", 13)
        self.c.setFillColor(NAVY)
        self.c.drawCentredString(PAGE_W / 2, self.y,
                                 "You don't need to install anything.")
        self.y -= 18
        self.c.drawCentredString(PAGE_W / 2, self.y,
                                 "You don't need to learn software.")
        self.y -= 26
        self.c.setFont("Inter-Bold", 16)
        self.c.setFillColor(RED)
        self.c.drawCentredString(PAGE_W / 2, self.y, "You just talk.")

        # ── Pull quote ──
        self.y -= 38
        self.draw_pull_quote(
            '"I built Mise because I wanted my restaurant back."',
            "\u2014 Jon Flaig, Co-Founder/CEO"
        )

        # ── Navy footer banner (bookend) ──
        footer_height = 80
        self.c.setFillColor(NAVY)
        self.c.rect(0, 0, PAGE_W, footer_height, fill=1, stroke=0)
        self.c.setStrokeColor(RED)
        self.c.setLineWidth(3)
        self.c.line(0, footer_height, PAGE_W, footer_height)
        # CTA
        self.c.setFont("Inter-Bold", 14)
        self.c.setFillColor(WHITE)
        self.c.drawCentredString(PAGE_W / 2, footer_height - 30,
                                 "Send completed form to: jon@getmise.io")
        self.c.setFont("Inter", 11)
        self.c.setFillColor(HexColor('#B8C4D8'))
        self.c.drawCentredString(PAGE_W / 2, footer_height - 48,
                                 "Questions? Call or text Jon directly.")
        # Tagline
        self.c.setFont("Inter-Italic", 8)
        self.c.setFillColor(HexColor('#7A8AA0'))
        self.c.drawCentredString(PAGE_W / 2, 10, "Mise: Everything in its place.")

        self.c.save()


def main():
    print("=" * 50)
    print("Generating: Fillable Onboarding Form")
    print("=" * 50)
    print()

    if LOGO_PATH.exists():
        print(f"Logo found: {LOGO_PATH}")
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}")
    print()

    output_path = OUTPUT_DIR / "Onboarding_Form_Fillable_020426.pdf"
    builder = MiseFormBuilder(output_path)
    builder.build()
    print(f"Saved to: {output_path}")

    # Copy to Google Drive
    if GDRIVE_LIBRARY.exists():
        dest = GDRIVE_LIBRARY / "Onboarding_Form_Fillable_020426.pdf"
        shutil.copy2(output_path, dest)
        print(f"Copied to Google Drive: {dest}")
    else:
        print(f"Google Drive path not found: {GDRIVE_LIBRARY}")

    print()
    print("=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    main()
