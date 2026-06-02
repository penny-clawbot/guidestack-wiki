#!/usr/bin/env python3
"""Generate essential legal/about pages for each site."""
import os, sys, json
from datetime import datetime

PROJECT_DIR = '/Users/penny/Documents/Penny/pseo-network'
REGISTRY = f'{PROJECT_DIR}/data/sites.json'

def generate_pages(site_name, niche):
    output_dir = f'{PROJECT_DIR}/data/content/{site_name}'
    os.makedirs(output_dir, exist_ok=True)
    
    date = datetime.now().strftime('%Y-%m-%d')
    site_title = niche.replace('-', ' ').title()
    
    # Privacy Policy
    privacy = f"""---
title: "Privacy Policy"
description: "Privacy policy for {site_title} — how we collect, use, and protect your information."
date: "{date}"
category: "legal"
tags: ["privacy", "policy"]
draft: false
readingTime: "3 min"
---

# Privacy Policy

**Last updated:** {datetime.now().strftime('%B %d, %Y')}

At {site_title}, we respect your privacy and are committed to protecting your personal data. This privacy policy explains how we collect, use, and safeguard your information when you visit our website.

## Information We Collect

### Automatically Collected Information
When you visit our website, we may automatically collect certain information about your device, including:
- Browser type and version
- Operating system
- IP address (anonymized)
- Pages visited and time spent on pages
- Referring website
- Device type (desktop, mobile, tablet)

### Information You Provide
- Email address (if you subscribe to our newsletter)
- Any information you voluntarily provide through contact forms

## How We Use Your Information

We use the information we collect to:
- Improve and personalize your experience on our website
- Analyze website usage to enhance content and functionality
- Send newsletters and updates (only if you opted in)
- Respond to your inquiries
- Maintain website security and prevent fraud

## Cookies and Tracking

We use cookies and similar tracking technologies to:
- Remember your preferences (e.g., dark mode setting)
- Analyze website traffic using privacy-respecting analytics
- Ensure website functionality

You can control cookies through your browser settings.

## Third-Party Services

We may use the following third-party services:
- **Analytics:** Privacy-focused analytics to understand website usage
- **Advertising:** Contextual ads that do not track you across websites
- **Email Service:** For delivering newsletters (only if subscribed)

These services may collect information as described in their own privacy policies.

## Data Security

We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction.

## Your Rights

You have the right to:
- Access the personal data we hold about you
- Request correction or deletion of your data
- Opt out of marketing communications
- Request a copy of your data in a portable format

## Children's Privacy

Our website is not directed at children under 13. We do not knowingly collect personal information from children.

## Changes to This Policy

We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the "Last updated" date.

## Contact Us

If you have questions about this privacy policy, please contact us through our website.

---

*This privacy policy is effective as of {datetime.now().strftime('%B %d, %Y')}.*
"""

    # About
    about = f"""---
title: "About Us"
description: "Learn about {site_title} — our mission, team, and commitment to providing the best {niche} content."
date: "{date}"
category: "about"
tags: ["about", "mission"]
draft: false
readingTime: "2 min"
---

# About {site_title}

{site_title} is your trusted resource for expert insights, practical tips, and comprehensive guides on {niche}. Our mission is to help you make informed decisions with content that is thoroughly researched, regularly updated, and genuinely helpful.

## Our Mission

We believe everyone deserves access to high-quality information. Whether you're just getting started or looking to deepen your expertise, our content is designed to provide real value — not clickbait or surface-level advice.

## What We Cover

- **Expert Guides:** In-depth articles written by specialists with real-world experience
- **Practical Tips:** Actionable advice you can apply immediately
- **Comparisons:** Honest, data-driven comparisons to help you choose
- **FAQs:** Clear answers to the questions people actually ask
- **How-To Guides:** Step-by-step instructions for {niche} topics

## Our Standards

Every piece of content on {site_title} meets these standards:

1. **Accuracy:** We verify facts, cite sources, and update outdated information
2. **Depth:** We go beyond surface-level to provide genuine expertise
3. **Actionability:** Every article should help you do something
4. **Honesty:** We present balanced views, including trade-offs and alternatives
5. **Freshness:** We regularly review and update our content

## Editorial Process

Our content goes through a multi-step process:
- **Research:** Thorough investigation of the topic
- **Writing:** Clear, engaging, expert-level content
- **Review:** Fact-checking and quality assurance
- **Publication:** With proper SEO optimization and formatting
- **Updates:** Regular review and revision

## Contact

Have a question, suggestion, or correction? We'd love to hear from you. Reach out through our website and we'll get back to you as soon as possible.

---

*Thank you for trusting {site_title} as your go-to resource for {niche}.*
"""

    # Terms of Service
    terms = f"""---
title: "Terms of Service"
description: "Terms and conditions for using {site_title}."
date: "{date}"
category: "legal"
tags: ["terms", "service"]
draft: false
readingTime: "3 min"
---

# Terms of Service

**Last updated:** {datetime.now().strftime('%B %d, %Y')}

Please read these terms of service carefully before using {site_title}. By accessing or using our website, you agree to be bound by these terms.

## Use of Our Website

{site_title} provides {niche} content for informational purposes. You agree to use our website only for lawful purposes and in accordance with these terms.

## Content Disclaimer

- Our content is for **informational purposes only** and should not be considered professional advice
- We strive for accuracy but make no warranties about the completeness or reliability of our content
- You should always do your own research and consult qualified professionals before making decisions
- Information about products, services, or strategies may change over time

## Intellectual Property

All content on {site_title}, including text, graphics, logos, and code, is our intellectual property or used with permission. You may not reproduce, distribute, or create derivative works without our written permission.

## User Conduct

You agree not to:
- Use our website for any unlawful purpose
- Attempt to gain unauthorized access to our systems
- Interfere with the proper functioning of our website
- Use automated tools to scrape or collect our content at scale

## Third-Party Links

Our website may contain links to third-party websites. We are not responsible for the content, privacy practices, or policies of external sites.

## Limitation of Liability

To the fullest extent permitted by law, {site_title} shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of our website.

## Changes to Terms

We reserve the right to modify these terms at any time. Continued use of our website after changes constitutes acceptance of the updated terms.

## Governing Law

These terms are governed by applicable laws. Any disputes shall be resolved through proper legal channels.

---

*By using {site_title}, you acknowledge that you have read and agree to these terms.*
"""

    # Write all pages
    for slug, content in [('privacy-policy', privacy), ('about', about), ('terms-of-service', terms)]:
        filepath = f'{output_dir}/{date}-ai-{slug}.md'
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  ✅ {slug}')

if __name__ == '__main__':
    with open(REGISTRY) as f:
        data = json.load(f)
    
    for site in data['sites']:
        if site['status'] == 'active':
            print(f"Generating legal pages for {site['name']}...")
            generate_pages(site['name'], site['niche'])
    print("Done!")
