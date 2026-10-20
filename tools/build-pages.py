"""Regenerate the static policy pages using the homepage's shared shell."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
home = (ROOT / "index.html").read_text(encoding="utf-8")
header = re.search(r"<header class=\"site-header\">.*?</header>", home, re.S).group()
footer = re.search(r"<footer class=\"site-footer\">.*?</footer>", home, re.S).group()
header = re.sub(r'href="#([^"]+)"', r'href="index.html#\1"', header)
footer = re.sub(r'href="#([^"]+)"', r'href="index.html#\1"', footer)

privacy = [
    ("scope", "01 / Scope and what UNMILD accesses",
     """<p>This policy covers Unmild Designer and this product website, published by <strong>UNMILD</strong>. The core Designer application works locally: it opens the project files and references you choose and stores your design and preferences on your computer. It does not require a Designer account, and the current core application has no built-in analytics, telemetry or cloud project sync.</p><p><strong>UNMILD does not automatically receive your board files, Mool programs or local project contents.</strong> If you contact support, we receive your email address, message and any files you choose to attach. Please send only what is needed to help with your request.</p>"""),
    ("flow", "02 / How the data flows",
     """<p>In the desktop application, your actions update a local project. Saving writes the project to your chosen location; exporting writes manufacturing and review files to its build folder. These actions do not upload the project to UNMILD.</p><p>Visiting this website sends ordinary web requests to its hosting provider. Following a Store link or sending a support email involves that service. If your project folder is inside a cloud-synced drive, your chosen drive service may synchronize it according to your settings.</p>"""),
    ("providers", "03 / Third-party AI providers",
     """<p>Designer’s core workflow does not require an AI provider or send prompts to one. If you independently use Unmild Agent or another AI tool with your design files, the content you authorize that tool to send is governed by that tool’s and the selected provider’s terms and privacy policy.</p><p>Before using an external provider, check its data use, retention, training and regional processing settings. This policy does not extend Designer’s local-only behavior to separate tools or services.</p>"""),
    ("keys", "04 / API keys and secrets",
     """<p>No AI API key is needed for Designer’s core design, Mool or export features. Do not place credentials in board notes, program examples, screenshots or support attachments. UNMILD support does not need your private keys or account passwords to answer product questions.</p><p>Credentials configured in a separate tool remain subject to that tool’s storage and security controls. Use the provider’s dashboard to revoke or replace an exposed key.</p>"""),
    ("website", "05 / Website, Store and support services",
     """<p>This website contains no advertising trackers, analytics scripts, embedded social feeds, account forms or application cookies. Fonts, images and scripts are served with the site; they do not request a third-party font service when you visit.</p><p>The site is prepared for GitHub Pages hosting. GitHub may process connection information such as IP addresses and request details under its <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">General Privacy Statement</a>. Microsoft handles Store installation, purchases and related account information under the <a href="https://www.microsoft.com/en-us/privacy/privacystatement">Microsoft Privacy Statement</a>. Email providers process messages you send through the support link under their own policies.</p><p>UNMILD uses information you send to support to respond, troubleshoot and follow up on your request. Where a legal basis is required, this is to provide requested support, pursue a legitimate interest in resolving product issues, or meet an applicable legal obligation. Optional information is used in the context in which you provide it.</p>"""),
    ("storage", "06 / Storage, retention and Smriti",
     """<p><strong>Designer:</strong> projects and export folders remain in the location you select until you move or delete them. Local preferences and recent-project information are saved in your Windows user profile. Uninstalling the app may leave projects, settings or backups behind. Deleting a local file does not necessarily delete synced copies or backups.</p><p><strong>Smriti:</strong> Smriti is the local conversation and working-context storage used by the separate Unmild Agent workflow; it is not Designer’s board format or a Designer cloud service. When using Agent alongside Designer, saved conversations and tool context may include information you supplied or allowed Agent to access. Manage those records in Agent and in its local storage, and manage provider-held copies separately under the provider’s policy.</p><p><strong>Support:</strong> messages and attachments may remain in the support mailbox and its backups while needed to resolve a request, maintain relevant support records or meet legal obligations. Ask UNMILD about a particular record or request deletion using the contact below. No fixed deletion period is promised for records retained by third-party services.</p>"""),
    ("sharing", "07 / Sharing and disclosure",
     """<p>UNMILD does not sell your personal information or automatically share local design files. Information you voluntarily send to support may be handled through the email service used to answer you. Information may also be disclosed where required by law, to protect legal rights or security, or with your permission.</p><p>You control when you export, email, publish or otherwise share a project. Review a file’s contents before giving it to a manufacturer, collaborator or external tool.</p>"""),
    ("security", "08 / Security measures",
     """<p>Keeping core design work local avoids an automatic project-upload path. You control access to your computer, project folders and backups through your operating system and storage settings. Protect the device, keep software current and use appropriate access controls for confidential designs.</p><p>Local storage is not a promise of file encryption, and no storage or communication system can guarantee absolute security. Do not send secrets through support email. Report a suspected security issue to <a href="mailto:unmildsupport@gmail.com?subject=Unmild%20Designer%20security">unmildsupport@gmail.com</a> with a description that omits private credentials.</p>"""),
    ("rights", "09 / Your privacy rights",
     """<p>You can manage, copy and delete your own local projects and exports. UNMILD cannot remotely retrieve or erase a file that exists only on your computer. Review Windows settings and any backup or synchronization service when managing other copies.</p><p>Depending on your location, you may have rights to access, correct, delete or receive a copy of personal information held by UNMILD, to restrict or object to its processing, or to withdraw consent where processing relies on consent. Contact us to exercise an applicable right. We may need to verify that a request concerns you; legal exceptions may apply. You may also contact your local data-protection authority.</p>"""),
    ("transfers", "10 / International transfers",
     """<p>The local Designer workflow does not itself transfer your project to another country. Website hosting, Store services, support email and any external provider you choose may process information in other countries. Their applicable privacy notices describe processing locations and transfer arrangements. Do not assume that separately shared information remains in the country where your device is located.</p>"""),
    ("children", "11 / Children and sensitive information",
     """<p>Designer is a technical design tool, and this website is not directed at children under 13 or the applicable minimum age for independent use in their region. If a child needs help contacting support, a parent or guardian should send the request. Contact UNMILD if you believe a child has sent us personal information that should be removed.</p><p>Do not include unnecessary personal, medical, financial or other sensitive information in project examples or support messages. Use particular care with proprietary engineering files and third-party confidential material.</p>"""),
    ("updates", "12 / Policy updates and contact",
     """<p>We may update this policy when the product, website or relevant practices change. The date at the top identifies the latest version. Material changes that require additional notice or consent will be handled as required by applicable law.</p><p><strong>Publisher: UNMILD.</strong><br>Privacy questions and requests: <a href="mailto:unmildsupport@gmail.com?subject=Unmild%20Designer%20privacy">unmildsupport@gmail.com</a>.<br>Product family: <a href="https://unmild.store">unmild.store</a>.</p>""")
]

terms = [
    ("agreement", "01 / Using Unmild Designer",
     """<p>These Terms of Use describe your use of the Unmild Designer website and software provided by <strong>UNMILD</strong>. By using them, you agree to these terms to the extent permitted by applicable law. If you do not agree, do not use the website or software. Any separate software license, purchase agreement and applicable Microsoft Store terms also govern the relevant transaction or installation.</p><p>You must be legally able to accept these terms, or use the software with appropriate permission and supervision. If you act for an organization, you must have authority to do so.</p>"""),
    ("license", "02 / License, projects and ownership",
     """<p>Subject to the license accompanying your copy, UNMILD permits you to install and use Designer for its intended design purposes. Buying or downloading the software does not transfer ownership of UNMILD’s software, name, branding or other intellectual property.</p><p>You retain the rights you hold in your own designs, programs and project content. You are responsible for having the permissions needed to use imported materials and share resulting exports. Third-party components and materials remain subject to their respective licenses.</p><p>Do not unlawfully redistribute the software, bypass license controls or misuse UNMILD’s branding. Nothing here restricts rights that applicable law gives you and does not allow a contract to waive.</p>"""),
    ("api", "03 / API keys and third-party providers",
     """<p>Designer’s core PCB, Mool and export workflow does not require AI API keys. If you choose to use a separate AI service, Unmild Agent, compiler, storage provider or other external tool with a project, you are responsible for that service’s account, permissions, fees and terms.</p><p>Keep credentials confidential, authorize only appropriate access and revoke exposed keys. UNMILD does not control third-party availability, charges, output, security practices or changes to their services. A link or compatible workflow does not transfer those responsibilities to UNMILD.</p>"""),
    ("autonomy", "04 / Agent autonomy and task execution",
     """<p>Designer is a desktop design workspace. Mool runs supported programs in the board-behavior environment; it is not an autonomous AI agent. Review the code, selected target and circuit before running a program.</p><p>If you independently allow an agent or automation tool to work on a Designer project, you decide its scope and permissions. Such tools may change files or execute actions within the access you grant. Review proposed actions and resulting changes, retain backups and do not grant access to material you are not authorized to share. The separate tool’s own terms govern its operation.</p>"""),
    ("responsibility", "05 / User responsibility and permissions",
     """<p>You are responsible for your design decisions, program behavior, file permissions and use of exported materials. Use Designer lawfully and respect intellectual-property, confidentiality, safety, export-control and other obligations that apply to your work.</p><p>Before manufacturing or operating hardware, independently review the board, part data, electrical constraints and manufacturer requirements. Keep backups of editable project files. Do not treat a generated export, passed check or visual preview as automatic approval for fabrication or deployment.</p>"""),
    ("privacy", "06 / Privacy and credential security",
     """<p>The <a href="privacy.html">Privacy Policy</a> explains local project storage, website hosting and information you voluntarily provide to support. Protect the Windows account and folders where you keep projects. You are responsible for any synchronization, backup or external sharing you configure.</p><p>Do not send account passwords, API keys, private signing keys or unrelated confidential files to support. Remove private information from screenshots and provide only the material needed to investigate an issue.</p>"""),
    ("limits", "07 / Engineering review and model boundaries",
     """<p>Designer’s previews, checks, calculations and simulation behavior are design aids. Results depend on the supported models, inputs and software version. Mool provides supported C/Arduino-style behavior; it does not certify processor timing or establish that code has been compiled or flashed to physical hardware.</p><p>Verify results using appropriate engineering methods, manufacturer specifications and physical testing. Designer is not offered as a certification service or a substitute for qualified review of safety-critical systems, regulated products or manufacturing acceptance.</p>"""),
    ("warranties", "08 / Warranties and liability",
     """<p>To the extent permitted by law, and except for warranties expressly included in your applicable purchase or license agreement, the website and software are provided “as is” and “as available.” UNMILD does not promise uninterrupted operation, error-free output or suitability for every design or manufacturing process.</p><p>To the extent permitted by applicable law, UNMILD is not liable for indirect or consequential losses, including lost profits, lost data, fabrication costs or business interruption arising from your use of the website or software.</p><p><strong>Nothing in these terms excludes liability or limits consumer rights that cannot lawfully be excluded or limited.</strong> Applicable mandatory warranties, remedies and statutory rights continue to apply.</p>"""),
    ("store", "09 / Availability, purchases and support",
     """<p>Pricing, regional availability, system requirements, payment and refund information are shown through the applicable Store or purchase agreement. Do not rely on screenshots or descriptions as a guarantee that every feature is available in every version.</p><p>UNMILD may improve or change the website and software over time. We welcome support requests and feedback, but do not promise a particular response time, feature delivery date or service level unless separately agreed in writing.</p>"""),
    ("updates", "10 / Updates and contact",
     """<p>UNMILD may revise these terms to reflect changes in the product, services or legal requirements. Updated terms will display a revised date. Material changes requiring notice or acceptance will be handled as required by applicable law.</p><p>If a provision cannot be enforced, the remaining terms continue to apply to the extent permitted by law. Mandatory local law and applicable purchase terms determine rights and dispute procedures that cannot be changed by these terms.</p><p><strong>Publisher: UNMILD.</strong><br>Questions: <a href="mailto:unmildsupport@gmail.com?subject=Unmild%20Designer%20terms">unmildsupport@gmail.com</a>.<br>Product family: <a href="https://unmild.store">unmild.store</a>.</p>""")
]

def page(filename, title, description, callout, sections):
    toc = "".join(f'<li><a href="#{key}">{heading}</a></li>' for key, heading, _ in sections)
    content = "\n".join(f'<section id="{key}"><h2>{heading}</h2>{body}</section>' for key, heading, body in sections)
    output = f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Unmild Designer</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#f3f2ec">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="css/style.css"><script src="js/main.js" defer></script>
</head>
<body><a class="skip-link" href="#main">Skip to content</a>
{header}
<main id="main" tabindex="-1">
<div class="container legal-intro">
<a class="back-link" href="index.html">← Back to Designer</a>
<p class="eyebrow">UNMILD / Clear by design</p>
<h1>{title}</h1><p class="lede">{description}</p>
<p class="legal-meta">Last updated: October 20, 2026 · Publisher: UNMILD</p>
</div>
<div class="container legal-layout">
<nav class="legal-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}</ol></nav>
<div class="legal-body"><div class="legal-callout"><p>{callout}</p></div>
{content}
<a class="text-link" href="#main">Back to top <span aria-hidden="true">↑</span></a>
</div></div></main>
{footer}
</body></html>
'''
    output = re.sub(r'<a href="(privacy|terms)\.html">', r'<a href="\1.html" target="_blank" rel="noopener noreferrer" aria-label="Read the \1 policy (opens in a new tab)">', output)
    (ROOT / filename).write_text(output, encoding="utf-8")

page("privacy.html", "Privacy Policy",
     "Your work stays local. Here is what happens when you use Designer, visit this website or get in touch.",
     "<strong>The core principle:</strong> Designer does not automatically upload your projects to UNMILD. Website hosting, Store services and information you choose to email are separate data flows, explained below.",
     privacy)
page("terms.html", "Terms of Use",
     "The terms for using Unmild Designer, with clear responsibilities for your projects, external tools and engineering decisions.",
     "<strong>Your work, your decisions.</strong> Designer helps you create and review electronics. You keep ownership of your content and responsibility for how you use it. Mandatory consumer rights remain protected.",
     terms)
print("Generated privacy.html and terms.html")
