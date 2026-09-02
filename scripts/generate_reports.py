"""Build three branded Week 3 Data Science Field Notes reports."""

from pathlib import Path

from PIL import Image as PillowImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
REPORT_DIR = ROOT / "reports"
BANNER_PATH = IMAGE_DIR / "wilson-moses-banner.png"
LOGO_PATH = IMAGE_DIR / "wilson-moses-logo.png"

PAGE_WIDTH, PAGE_HEIGHT = A4
DARK = colors.HexColor("#0d0d0d")
OFF_WHITE = colors.HexColor("#f4f0e8")
PAPER = colors.HexColor("#fbfaf7")
GREY = colors.HexColor("#6f6d68")
LIGHT_GREY = colors.HexColor("#dedbd3")
GOLD = colors.HexColor("#c69a4b")


def register_fonts() -> None:
    fonts = {
        "BrandSans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "BrandSansBold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "BodySerif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "BodySerifBold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "BodySerifItalic": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    }
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, path))


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "cover_eyebrow": ParagraphStyle("cover_eyebrow", parent=base["Normal"], fontName="BrandSansBold", fontSize=10, leading=14, textColor=GOLD, spaceAfter=6, tracking=1.2),
        "cover_title": ParagraphStyle("cover_title", parent=base["Title"], fontName="BrandSansBold", fontSize=27, leading=32, textColor=OFF_WHITE, alignment=TA_LEFT, spaceAfter=12),
        "cover_subtitle": ParagraphStyle("cover_subtitle", parent=base["Normal"], fontName="BodySerif", fontSize=11.5, leading=17, textColor=colors.HexColor("#c7c4bd"), spaceAfter=18),
        "cover_meta": ParagraphStyle("cover_meta", parent=base["Normal"], fontName="BrandSans", fontSize=8.6, leading=13, textColor=OFF_WHITE),
        "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="BrandSansBold", fontSize=16.2, leading=20, textColor=DARK, spaceBefore=2, spaceAfter=8, keepWithNext=True),
        "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="BrandSansBold", fontSize=11.8, leading=15, textColor=colors.HexColor("#8b6426"), spaceBefore=7, spaceAfter=5, keepWithNext=True),
        "body": ParagraphStyle("body", parent=base["BodyText"], fontName="BodySerif", fontSize=9.7, leading=14.2, textColor=colors.HexColor("#252422"), alignment=TA_LEFT, spaceAfter=6),
        "callout": ParagraphStyle("callout", parent=base["BodyText"], fontName="BodySerifItalic", fontSize=9.7, leading=14.2, leftIndent=10, rightIndent=10, borderPadding=9, backColor=colors.HexColor("#f1e8d8"), textColor=colors.HexColor("#3a3329"), spaceBefore=3, spaceAfter=10),
        "caption": ParagraphStyle("caption", parent=base["Normal"], fontName="BrandSans", fontSize=7.8, leading=10, textColor=GREY, alignment=TA_CENTER, spaceBefore=3, spaceAfter=7),
        "table_header": ParagraphStyle("table_header", parent=base["Normal"], fontName="BrandSansBold", fontSize=7.8, leading=10, textColor=OFF_WHITE),
        "table_cell": ParagraphStyle("table_cell", parent=base["Normal"], fontName="BodySerif", fontSize=7.8, leading=10.5, textColor=colors.HexColor("#252422")),
        "small": ParagraphStyle("small", parent=base["Normal"], fontName="BrandSans", fontSize=7.8, leading=10.5, textColor=GREY),
    }


def draw_cover(canvas, _doc) -> None:
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    canvas.setFillColor(GOLD)
    canvas.rect(18 * mm, 18 * mm, 1.6 * mm, PAGE_HEIGHT - 36 * mm, stroke=0, fill=1)
    canvas.restoreState()


def draw_body_page(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    canvas.setFillColor(DARK)
    canvas.rect(0, PAGE_HEIGHT - 21 * mm, PAGE_WIDTH, 21 * mm, stroke=0, fill=1)
    canvas.drawImage(str(LOGO_PATH), PAGE_WIDTH - 39 * mm, PAGE_HEIGHT - 18 * mm, 28 * mm, 13 * mm, preserveAspectRatio=True, mask="auto")
    canvas.setFont("BrandSansBold", 8.7)
    canvas.setFillColor(OFF_WHITE)
    canvas.drawString(18 * mm, PAGE_HEIGHT - 10.2 * mm, "WILSON MOSES")
    canvas.setFont("BrandSans", 7.6)
    canvas.setFillColor(GOLD)
    canvas.drawString(18 * mm, PAGE_HEIGHT - 15.2 * mm, "DATA SCIENCE FIELD NOTES")
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.8)
    canvas.line(18 * mm, 15 * mm, PAGE_WIDTH - 18 * mm, 15 * mm)
    canvas.setFont("BrandSans", 7.2)
    canvas.setFillColor(GREY)
    canvas.drawString(18 * mm, 9.5 * mm, doc.report_short_title)
    canvas.drawRightString(PAGE_WIDTH - 18 * mm, 9.5 * mm, f"{doc.page - 1:02d}")
    canvas.restoreState()


def report_document(path: Path, short_title: str) -> BaseDocTemplate:
    body_frame = Frame(18 * mm, 17 * mm, PAGE_WIDTH - 36 * mm, PAGE_HEIGHT - 42 * mm, id="body", leftPadding=0, rightPadding=0, topPadding=2 * mm, bottomPadding=2 * mm)
    cover_frame = Frame(27 * mm, 22 * mm, PAGE_WIDTH - 49 * mm, PAGE_HEIGHT - 40 * mm, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    document = BaseDocTemplate(str(path), pagesize=A4, title=path.stem.replace("_", " ").title(), author="Wilson Moses", subject="Loan approval analysis and feature engineering portfolio report", creator="Wilson Moses")
    document.report_short_title = short_title
    document.addPageTemplates([PageTemplate(id="Cover", frames=[cover_frame], onPage=draw_cover), PageTemplate(id="Body", frames=[body_frame], onPage=draw_body_page)])
    return document


def cover_story(styles, number: str, title: str, subtitle: str) -> list:
    banner = Image(str(BANNER_PATH), width=155 * mm, height=38.75 * mm)
    metadata = Table(
        [
            [Paragraph("AUTHOR", styles["small"]), Paragraph("Wilson Moses", styles["cover_meta"])],
            [Paragraph("PROGRAMME", styles["small"]), Paragraph("AnalystLab Africa - Data Science Internship", styles["cover_meta"])],
            [Paragraph("PROJECT", styles["small"]), Paragraph("Loan Approval Analysis and Feature Engineering", styles["cover_meta"])],
            [Paragraph("PHASE", styles["small"]), Paragraph("Week 3 | Completed analytical preparation", styles["cover_meta"])],
        ],
        colWidths=[32 * mm, 107 * mm],
        hAlign="LEFT",
    )
    metadata.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#171717")), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")), ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#333333")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return [
        Spacer(1, 7 * mm), banner, Spacer(1, 31 * mm),
        Paragraph(f"DATA SCIENCE FIELD NOTES / {number}", styles["cover_eyebrow"]),
        Paragraph(title, styles["cover_title"]),
        Paragraph(subtitle, styles["cover_subtitle"]),
        HRFlowable(width="100%", thickness=1.2, color=GOLD, spaceBefore=1, spaceAfter=14),
        metadata, Spacer(1, 22 * mm),
        Paragraph("Educational portfolio report. Historical approval patterns do not constitute a production lending model or lending policy.", styles["cover_subtitle"]),
        NextPageTemplate("Body"), PageBreak(),
    ]


def heading(text: str, styles) -> Paragraph:
    return Paragraph(text, styles["h1"])


def subheading(text: str, styles) -> Paragraph:
    return Paragraph(text, styles["h2"])


def body(text: str, styles) -> Paragraph:
    return Paragraph(text, styles["body"])


def callout(text: str, styles) -> Paragraph:
    return Paragraph(text, styles["callout"])


def bullet_list(items: list[str], styles) -> ListFlowable:
    return ListFlowable([ListItem(Paragraph(item, styles["body"]), leftIndent=10) for item in items], bulletType="bullet", start="circle", leftIndent=18, bulletFontName="BodySerif", bulletFontSize=7, spaceAfter=7)


def styled_table(rows: list[list[str]], widths: list[float], styles) -> Table:
    formatted = []
    for index, row in enumerate(rows):
        style = styles["table_header"] if index == 0 else styles["table_cell"]
        formatted.append([Paragraph(str(value), style) for value in row])
    table = Table(formatted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK), ("TEXTCOLOR", (0, 0), (-1, 0), OFF_WHITE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f0eee8")]), ("GRID", (0, 0), (-1, -1), 0.35, LIGHT_GREY), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return table


def report_image(filename: str, width: float, styles, caption: str) -> list:
    path = IMAGE_DIR / filename
    with PillowImage.open(path) as source:
        ratio = source.height / source.width
    return [Image(str(path), width=width, height=width * ratio), Paragraph(caption, styles["caption"])]


def new_page() -> PageBreak:
    return PageBreak()


def build_business_report(styles) -> None:
    story = cover_story(styles, "03A", "BUSINESS INSIGHTS REPORT", "Evidence-led findings, responsible interpretation and decisions for the next modelling phase")
    story += [
        heading("Executive summary", styles),
        body("This report evaluates 614 historical loan applications to identify the factors most closely associated with approval and to prepare a responsible foundation for predictive modelling. Of the applications, 422 were approved and 192 were rejected, producing a historical approval rate of 68.73%.", styles),
        callout("Principal finding: applicants with positive credit history recorded a 79.05% approval rate, compared with 7.87% for applicants without positive credit history.", styles),
        styled_table([["Portfolio measure", "Verified result"], ["Applications analysed", "614"], ["Approved / rejected", "422 / 192"], ["Historical approval rate", "68.73%"], ["Training / test observations", "491 / 123"], ["Engineered features", "12"]], [82 * mm, 85 * mm], styles),
        Spacer(1, 5 * mm),
        *report_image("credit-history-approval.png", 147 * mm, styles, "Figure 1. Historical approval rate by recorded credit-history status."),
        new_page(),
        heading("Business context and analytical approach", styles),
        body("Lending institutions must balance access to credit with consistent risk assessment. This project examines whether applicant characteristics, household income, requested loan size, credit information and property area show meaningful relationships with historical approval decisions.", styles),
        body("The workflow combines quality validation, exploratory visualisation, six hypothesis tests, feature engineering, responsible feature selection and leakage-safe preparation. It does not estimate repayment performance or actual default risk.", styles),
        subheading("Credit history is the dominant observed factor", styles),
        body("The relationship between credit history and approval is statistically significant (chi-square = 176.115; p < 0.001). Cramer's V of 0.536 is materially stronger than the other tested categorical association. Credit-history completeness and verification should therefore remain central to later modelling and data-quality controls.", styles),
        subheading("Property area is a weaker secondary signal", styles),
        body("Approval rates are 76.82% in semiurban areas, 65.84% in urban areas and 61.45% in rural areas. The association is statistically significant (p = 0.002), but Cramer's V is only 0.142. Geographic differences require investigation before they influence policy or operations.", styles),
        *report_image("property-area-approval.png", 143 * mm, styles, "Figure 2. Property-area rates differ, but the association is much weaker than credit history."),
        new_page(),
        heading("What the financial variables reveal", styles),
        body("Total household income and requested loan amount do not differ significantly between approved and rejected applications when assessed separately. Total income yields p = 0.713 and loan amount yields p = 0.398. These results do not make financial information irrelevant; they show that isolated raw values do not explain historical outcomes in this sample.", styles),
        body("Total income and requested loan amount are strongly related (Spearman rho = 0.688; p < 0.001). Higher-income households generally request larger loans. Affordability should therefore be examined as a relationship among income, amount and repayment term rather than as an isolated threshold.", styles),
        *report_image("income-loan-relationship.png", 148 * mm, styles, "Figure 3. Household income and requested loan amount show a strong positive monotonic relationship."),
        subheading("Feature-engineering decisions", styles),
        bullet_list(["Payment-income ratio combines approximate monthly principal, income and term into an affordability proxy.", "Coapplicant-income share describes dependence on a second income source.", "Log transformations reduce the influence of highly skewed financial values.", "Readable household, income and credit categories support communication but are controlled for redundancy in modelling."], styles),
        new_page(),
        heading("Recommended actions", styles),
        bullet_list(["Prioritise completeness and verification of credit-history information.", "Assess affordability through combined repayment and income indicators.", "Investigate geographic differences for product, branch-policy or data-collection effects.", "Monitor demographic fairness without using gender as a predictive input.", "Preserve the predetermined test partition and fit every transformation on training data only."], styles),
        heading("Limitations and responsible interpretation", styles),
        bullet_list(["The dataset contains only 614 applications, so estimates for smaller groups may be unstable.", "Historical approval is the target, not repayment performance or default risk.", "Interest rates, existing debt, expenses and verified monthly instalments are unavailable.", "Previously imputed values may reduce natural variation.", "Application dates and applicant identifiers are absent, limiting temporal and repeat-applicant analysis.", "Observed associations may reflect historical institutional bias and do not establish causation."], styles),
        heading("Next steps", styles),
        bullet_list(["Train a transparent baseline before comparing more complex classifiers.", "Use stratified cross-validation and evaluate precision, recall, F1, ROC-AUC and calibration.", "Audit subgroup errors and document threshold trade-offs.", "Keep human review, lending policy and compliance controls outside the model."], styles),
        heading("Conclusion", styles),
        body("The Week 3 investigation transforms a cleaned application dataset into a statistically examined, feature-engineered and modelling-ready resource. Credit history is the clearest observed approval factor, while property area contributes a smaller signal and financial variables become more informative when combined into affordability-oriented representations.", styles),
    ]
    report_document(REPORT_DIR / "business_insights_report.pdf", "LOAN APPROVAL / BUSINESS INSIGHTS").build(story)


def build_statistical_report(styles) -> None:
    story = cover_story(styles, "03B", "STATISTICAL ANALYSIS REPORT", "Six hypothesis tests separating strong evidence, weak signals and unsupported differences")
    story += [
        heading("Analytical scope", styles),
        body("Six hypothesis tests evaluate categorical associations, differences between approved and rejected groups, geographic income variation and the relationship between household income and requested loan amount.", styles),
        styled_table([["Analytical element", "Application"], ["Significance threshold", "alpha = 0.05"], ["Categorical association", "Chi-square test of independence"], ["Two skewed numerical groups", "Mann-Whitney U test"], ["Three skewed numerical groups", "Kruskal-Wallis test"], ["Monotonic numerical relationship", "Spearman rank correlation"], ["Categorical effect size", "Cramer's V"]], [68 * mm, 99 * mm], styles),
        heading("Assumption assessment", styles),
        body("Income and loan variables are strongly right-skewed and contain plausible extreme observations. Normality checks and visual inspection support nonparametric rank-based comparisons. Expected contingency-table counts exceed common minimum thresholds for the chi-square tests.", styles),
        callout("Interpretation rule: a small p-value supports an association or group difference. It does not establish causation, business importance, fairness or legal permissibility.", styles),
        new_page(),
        heading("Test 1 - Credit history and approval", styles),
        body("H0: credit history and approval are independent. H1: they are associated.", styles),
        styled_table([["Credit history", "Rejected", "Approved", "Approval rate"], ["0 - No positive history", "82", "7", "7.87%"], ["1 - Positive history", "110", "415", "79.05%"]], [65 * mm, 30 * mm, 30 * mm, 42 * mm], styles),
        body("Result: chi-square = 176.115; df = 1; p = 3.418e-40; Cramer's V = 0.536; minimum expected count = 27.83. Reject H0. Credit history has a strong observed relationship with historical approval.", styles),
        *report_image("credit-history-approval.png", 140 * mm, styles, "Figure 1. The largest observed approval-rate separation in the analysis."),
        subheading("Test 2 - Property area and approval", styles),
        body("H0: property area and approval are independent. H1: they are associated.", styles),
        styled_table([["Property area", "Rejected", "Approved", "Approval rate"], ["Semiurban", "54", "179", "76.82%"], ["Urban", "69", "133", "65.84%"], ["Rural", "69", "110", "61.45%"]], [65 * mm, 30 * mm, 30 * mm, 42 * mm], styles),
        body("Result: chi-square = 12.298; df = 2; p = 0.0021; Cramer's V = 0.142. Reject H0, but treat property area as a weak secondary signal.", styles),
        new_page(),
        heading("Test 3 - Total income by approval outcome", styles),
        body("H0: total-income distributions are equivalent across outcomes. H1: the distributions differ.", styles),
        styled_table([["Outcome", "Observations", "Median total income"], ["Approved", "422", "5,439.00"], ["Rejected", "192", "5,289.50"]], [65 * mm, 42 * mm, 60 * mm], styles),
        body("Mann-Whitney U = 41,262.5; p = 0.7128; rank-biserial effect = -0.019. Do not reject H0. Total income does not independently distinguish historical outcomes in this sample.", styles),
        heading("Test 4 - Loan amount by approval outcome", styles),
        body("H0: requested loan-amount distributions are equivalent across outcomes. H1: the distributions differ.", styles),
        styled_table([["Outcome", "Observations", "Median loan amount"], ["Approved", "422", "128.00"], ["Rejected", "192", "128.00"]], [65 * mm, 42 * mm, 60 * mm], styles),
        body("Mann-Whitney U = 38,788.0; p = 0.3976; rank-biserial effect = 0.043. Do not reject H0. Loan size should not be interpreted in isolation.", styles),
        callout("Non-significance does not prove that a feature is useless. Income and amount may contribute through interactions or engineered relationships.", styles),
        new_page(),
        heading("Test 5 - Total income across property areas", styles),
        body("H0: rural, urban and semiurban applicants have equivalent total-income distributions. H1: at least one group differs.", styles),
        styled_table([["Property area", "Observations", "Median total income"], ["Rural", "179", "5,704.00"], ["Semiurban", "233", "5,191.00"], ["Urban", "202", "5,258.50"]], [65 * mm, 42 * mm, 60 * mm], styles),
        body("Kruskal-Wallis H = 3.933; p = 0.1400. Do not reject H0. The observed area-level approval differences cannot be attributed solely to distinguishable total-income distributions.", styles),
        heading("Test 6 - Income and requested loan amount", styles),
        body("H0: there is no monotonic relationship between total household income and requested loan amount. H1: a relationship exists.", styles),
        body("Spearman rho = 0.688; p = 3.423e-87. Reject H0. Higher-income applicants generally request larger loans. The result supports income-relative affordability features but does not show that income causes approval.", styles),
        *report_image("income-loan-relationship.png", 145 * mm, styles, "Figure 2. Strong positive monotonic relationship between household income and requested amount."),
        new_page(),
        heading("Consolidated statistical results", styles),
        styled_table([["Analysis", "Statistic", "p-value", "Decision"], ["Credit history vs approval", "176.115", "<0.001", "Reject H0"], ["Property area vs approval", "12.298", "0.002", "Reject H0"], ["Total income by approval", "41,262.5", "0.713", "Do not reject"], ["Loan amount by approval", "38,788.0", "0.398", "Do not reject"], ["Income across property areas", "3.933", "0.140", "Do not reject"], ["Income vs loan amount", "0.688", "<0.001", "Reject H0"]], [70 * mm, 34 * mm, 28 * mm, 35 * mm], styles),
        heading("Effect size and practical significance", styles),
        body("Credit history combines a very small p-value with a comparatively strong effect size. Property area is statistically significant but much weaker, so it should not receive equal operational weight. The income and loan-amount group comparisons have very small rank-biserial effects.", styles),
        heading("Interpretation controls", styles),
        bullet_list(["Multiple tests were conducted; borderline results require cautious interpretation and later validation.", "The target records historical approvals rather than repayment or default.", "Non-significance does not rule out predictive value in interaction with other variables.", "Statistical association does not establish a causal or legally permissible lending criterion."], styles),
        heading("Conclusion", styles),
        body("The evidence supports prioritising credit history, retaining property area as a secondary candidate, engineering income-relative affordability indicators and validating every conclusion through out-of-sample modelling and fairness checks.", styles),
    ]
    report_document(REPORT_DIR / "statistical_analysis_report.pdf", "LOAN APPROVAL / STATISTICAL ANALYSIS").build(story)


def build_feature_report(styles) -> None:
    story = cover_story(styles, "03C", "FEATURE ENGINEERING DOCUMENTATION", "Twelve interpretable features, controlled redundancy and leakage-safe preprocessing")
    story += [
        heading("Purpose and scope", styles),
        body("Feature engineering improves the interpretability and modelling usefulness of the upstream cleaned dataset. The work introduces 12 representations covering dependents, household structure, income segmentation, coapplicant contribution, repayment burden, credit interpretation and financial transformations.", styles),
        callout("Design principle: a useful engineered feature needs a clear business interpretation, valid construction, defensible modelling benefit and documented limitation.", styles),
        styled_table([["Project measure", "Verified result"], ["Upstream cleaned observations", "614"], ["Upstream cleaned columns", "14"], ["Engineered features", "12"], ["Final analytical columns", "26"], ["Selected source modelling features", "12"], ["Final encoded predictors", "13"]], [88 * mm, 79 * mm], styles),
        heading("Data and unit considerations", styles),
        body("The upstream loan_income_ratio divides a loan amount recorded in thousands by monthly income in currency units, so the units are not directly comparable. The improved payment-income proxy first converts the recorded amount into currency units and then divides it by the repayment term.", styles),
        new_page(),
        heading("Feature catalogue - Household and income", styles),
        styled_table([["Feature", "Construction", "Interpretation"], ["dependents_numeric", "Map 3+ conservatively to 3", "Machine-readable dependent count"], ["family_size", "1 + married indicator + dependents", "Approximate household responsibility"], ["family_size_group", "Small / Medium / Large", "Readable household segment"], ["income_band", "Low / Middle / High / Very High", "Readable income segment"], ["has_coapplicant_income", "1 if coapplicant income > 0", "Single- vs dual-income signal"], ["coapplicant_income_share", "Coapplicant income / total income", "Dependence on shared income"]], [49 * mm, 57 * mm, 61 * mm], styles),
        heading("Interpretation notes", styles),
        body("The 3+ dependents category is mapped to 3 because the exact value is unavailable, so family size remains an approximation. Fixed income-band thresholds require review before use in another market or currency context. Zero coapplicant income is a valid observation, not a missing value.", styles),
        heading("Selection decision", styles),
        bullet_list(["Retain dependents_numeric, has_coapplicant_income and coapplicant_income_share for modelling.", "Keep family_size, family_size_group and income_band for analytical reporting.", "Avoid combining family_size with every exact source component when unnecessary."], styles),
        new_page(),
        heading("Feature catalogue - Credit, duration and affordability", styles),
        styled_table([["Feature", "Construction", "Interpretation"], ["term_years", "Loan term in months / 12", "Readable duration"], ["estimated_monthly_principal", "Loan amount x 1,000 / term", "Approximate principal instalment"], ["payment_income_ratio", "Estimated principal / total income", "Repayment-burden proxy"], ["credit_risk_category", "Readable label from credit history", "Stakeholder-facing category"], ["log_total_income", "Natural log of 1 + total income", "Reduced income skewness"], ["log_loan_amount", "Natural log of 1 + loan amount", "Reduced amount skewness"]], [49 * mm, 57 * mm, 61 * mm], styles),
        heading("Affordability proxy example", styles),
        body("For the first application, a recorded amount of 128 represents approximately 128,000 currency units. Dividing by a 360-month term gives estimated principal of 355.56 per month. Dividing by total income of 5,849 produces a payment-income proxy of 6.08%.", styles),
        callout("The proxy excludes interest, insurance, existing debt and other obligations. It is suitable as an analytical feature, not as a complete underwriting decision." , styles),
        heading("Redundancy controls", styles),
        bullet_list(["Retain credit_history for modelling and credit_risk_category for reporting.", "Retain term_years instead of duplicating the original month-based term.", "Use log_total_income and log_loan_amount instead of their raw equivalents in the model inputs.", "Represent estimated monthly principal within payment_income_ratio rather than retaining both."], styles),
        new_page(),
        heading("Final selected modelling inputs", styles),
        styled_table([["Feature family", "Selected inputs"], ["Applicant context", "married; dependents_numeric; education; self_employed"], ["Location and credit", "property_area; credit_history"], ["Financial transformations", "log_total_income; log_loan_amount; term_years"], ["Household and affordability", "has_coapplicant_income; coapplicant_income_share; payment_income_ratio"]], [54 * mm, 113 * mm], styles),
        heading("Responsible modelling decision", styles),
        body("Gender is excluded from predictive inputs because it can act as a protected characteristic and reproduce historical bias. It remains available in the analytical dataset for subgroup fairness auditing.", styles),
        heading("Leakage-safe preprocessing", styles),
        bullet_list(["Split 614 applications into 491 training and 123 testing rows using stratified sampling.", "Fit one-hot encoding on training categories only and ignore unseen test categories.", "Fit standard scaling on training values of continuous engineered features only.", "Pass binary and ordinal variables through without unnecessary scaling.", "Publish cleaned, combined ML-ready, training and testing datasets with a data dictionary."], styles),
        heading("Conclusion", styles),
        body("The final feature set combines statistical evidence with interpretable financial relationships, controlled redundancy, fairness awareness and reproducible train/test preprocessing. It prepares the project for careful model comparison without claiming production readiness.", styles),
    ]
    report_document(REPORT_DIR / "feature_engineering_documentation.pdf", "LOAN APPROVAL / FEATURE ENGINEERING").build(story)


def main() -> None:
    register_fonts()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    build_business_report(styles)
    build_statistical_report(styles)
    build_feature_report(styles)
    print("Created three branded Week 3 Data Science Field Notes reports.")


if __name__ == "__main__":
    main()
