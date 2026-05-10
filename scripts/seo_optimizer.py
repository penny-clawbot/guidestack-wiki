#!/usr/bin/env python3
"""
SEO Optimizer - Validate and optimize generated content for search engines
Ensures keyword density, readability, schema markup, and frontmatter completeness
"""

import sys
import os
import re
from typing import Dict, List, Tuple


def analyze_keyword_density(content: str, keyword: str) -> Tuple[float, str]:
    """Calculate keyword density percentage. Target: 1-2%."""
    words = re.findall(r'\w+', content.lower())
    total_words = len(words)
    
    if total_words == 0:
        return 0.0, "No content to analyze"
    
    keyword_lower = keyword.lower()
    keyword_words = keyword_lower.split()
    
    # Count keyword occurrences (including multi-word)
    occurrences = 0
    content_lower = content.lower()
    
    for i in range(len(words) - len(keyword_words) + 1):
        phrase = ' '.join(words[i:i + len(keyword_words)])
        if phrase == keyword_lower:
            occurrences += 1
    
    density = (occurrences / total_words) * 100
    
    if density < 0.5:
        status = "LOW - consider adding more keyword mentions"
    elif density > 3:
        status = "HIGH - reduce keyword usage to avoid over-optimization"
    else:
        status = "OK - good keyword density"
    
    return round(density, 2), status


def check_readability(content: str) -> Dict[str, any]:
    """Check content readability metrics."""
    lines = content.split('\n')
    
    # Count paragraphs
    paragraphs = [l for l in lines if l.strip() and not l.startswith('#')]
    avg_para_length = sum(len(p.split()) for p in paragraphs) / max(len(paragraphs), 1)
    
    # Check for bullet points (good for scannability)
    bullets = len(re.findall(r'^[\s]*[-*]\s', content, re.MULTILINE))
    
    # Check for short sentences (recommended: < 25 words)
    long_sentences = 0
    for para in paragraphs:
        sentences = re.split(r'[.!?]+', para)
        for sent in sentences:
            if len(sent.split()) > 25:
                long_sentences += 1
    
    recommendations = []
    
    if avg_para_length > 50:
        recommendations.append("Consider breaking long paragraphs into shorter ones (aim for 3-4 sentences each)")
    
    if bullets < 3:
        recommendations.append("Add bullet points to improve scannability")
    
    if long_sentences > 10:
        recommendations.append(f"Found {long_sentences} sentences over 25 words - consider breaking them up")
    
    return {
        "avg_paragraph_length": round(avg_para_length, 1),
        "paragraph_count": len(paragraphs),
        "bullet_points": bullets,
        "long_sentences": long_sentences,
        "recommendations": recommendations
    }


def extract_headings(content: str) -> List[Dict[str, str]]:
    """Extract all headings with their levels."""
    headings = []
    for line in content.split('\n'):
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({"level": level, "text": text})
    return headings


def validate_frontmatter(frontmatter: str) -> Dict[str, any]:
    """Validate frontmatter has required fields."""
    required = ["title", "description", "date", "category"]
    optional = ["tags", "image", "draft", "readingTime"]
    
    issues = []
    present = []
    missing = []
    
    for field in required:
        pattern = rf'^{field}:\s*["\']?(.+?)(["\']?)\s*$'
        if re.search(pattern, frontmatter, re.MULTILINE):
            present.append(field)
        else:
            missing.append(field)
            issues.append(f"Missing required field: {field}")
    
    # Check description length
    desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)', frontmatter)
    if desc_match:
        desc_len = len(desc_match.group(1))
        if desc_len > 160:
            issues.append(f"Meta description too long ({desc_len} chars, max 160)")
        elif desc_len < 120:
            issues.append(f"Meta description short ({desc_len} chars, consider expanding to 150-160)")
    
    return {
        "valid": len(missing) == 0,
        "present": present,
        "missing": missing,
        "issues": issues
    }


def suggest_image_alt_text(content: str) -> List[Dict[str, str]]:
    """Suggest alt text for images based on surrounding content."""
    # This is a simplified version - full implementation would analyze image contexts
    suggestions = []
    
    # Find headings to suggest contextual images
    headings = extract_headings(content)
    for h in headings:
        if h["level"] == 2:  # H2 sections often need images
            suggestions.append({
                "section": h["text"],
                "alt_text": f"Image describing {h['text']}",
                "placeholder": f"![{h['text']}](image-url.jpg)"
            })
    
    return suggestions


def suggest_schema_markup(frontmatter: str, article_type: str) -> str:
    """Generate schema.org markup suggestions based on article type."""
    
    type_schemas = {
        "faq": '''{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Your question here?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Your answer here."
      }
    }
  ]
}''',
        "howto": '''{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Step 1",
      "text": "Description of step 1"
    },
    {
      "@type": "HowToStep", 
      "name": "Step 2",
      "text": "Description of step 2"
    }
  ]
}''',
        "listicle": '''{
  "@context": "https://schema.org", 
  "@type": "Article",
  "headline": "Your article title",
  "description": "Brief description",
  "datePublished": "2026-05-10"
}''',
        "pillar": '''{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Your pillar article title",
  "description": "Comprehensive guide description",
  "datePublished": "2026-05-10"
}'''
    }
    
    return type_schemas.get(article_type, type_schemas["pillar"])


def optimize_content(filepath: str) -> Dict[str, any]:
    """Run full SEO analysis on a content file."""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split frontmatter and content
    if content.startswith('---'):
        parts = content.split('---', 2)
        frontmatter = parts[1] if len(parts) > 1 else ""
        body = parts[2] if len(parts) > 2 else content
    else:
        frontmatter = ""
        body = content
    
    # Extract keyword from frontmatter or filename
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)', frontmatter)
    keyword = title_match.group(1) if title_match else os.path.basename(filepath)
    
    # Run all checks
    density, density_status = analyze_keyword_density(body, keyword)
    readability = check_readability(body)
    fm_validation = validate_frontmatter(frontmatter) if frontmatter else {"valid": False, "issues": ["No frontmatter found"]}
    headings = extract_headings(content)
    alt_suggestions = suggest_image_alt_text(body)
    
    return {
        "file": filepath,
        "keyword_density": density,
        "density_status": density_status,
        "readability": readability,
        "frontmatter": fm_validation,
        "headings": headings,
        "alt_text_suggestions": alt_suggestions
    }


def print_report(report: Dict) -> None:
    """Print formatted SEO report."""
    print("\n" + "=" * 60)
    print(f"SEO Analysis: {report['file']}")
    print("=" * 60)
    
    print(f"\n📊 KEYWORD DENSITY")
    print(f"   Density: {report['keyword_density']}%")
    print(f"   Status: {report['density_status']}")
    
    print(f"\n📝 FRONTMATTER VALIDATION")
    fm = report['frontmatter']
    print(f"   Valid: {'✓' if fm['valid'] else '✗'}")
    if fm.get('present'):
        print(f"   Present: {', '.join(fm['present'])}")
    if fm.get('missing'):
        print(f"   Missing: {', '.join(fm['missing'])}")
    if fm.get('issues'):
        print(f"   Issues:")
        for issue in fm['issues']:
            print(f"     - {issue}")
    
    print(f"\n📖 READABILITY")
    r = report['readability']
    print(f"   Avg paragraph length: {r['avg_paragraph_length']} words")
    print(f"   Paragraphs: {r['paragraph_count']}")
    print(f"   Bullet points: {r['bullet_points']}")
    if r['recommendations']:
        print(f"   Recommendations:")
        for rec in r['recommendations']:
            print(f"     • {rec}")
    
    print(f"\n🏗️ HEADINGS STRUCTURE")
    for h in report['headings']:
        indent = "  " * (h['level'] - 1)
        print(f"   {indent}H{h['level']}: {h['text']}")
    
    if report['alt_text_suggestions']:
        print(f"\n🖼️ IMAGE ALT TEXT SUGGESTIONS")
        for alt in report['alt_text_suggestions'][:5]:
            print(f"   Section: {alt['section']}")
            print(f"   Alt: {alt['alt_text']}")
            print()


def main():
    if len(sys.argv) < 2:
        print("Usage: seo-optimizer.py <content_file.md> [keywords...]")
        print("Example: seo-optimizer.py article.md 'smart thermostat' 'energy savings'")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        sys.exit(1)
    
    report = optimize_content(filepath)
    print_report(report)


if __name__ == "__main__":
    main()