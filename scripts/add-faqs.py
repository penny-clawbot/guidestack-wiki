#!/usr/bin/env python3
"""Append FAQ sections to existing articles that don't have them.
Uses pattern matching on the article title to generate relevant FAQs."""
import os, re, glob

PROJECT_DIR = "/Users/penny/Documents/Penny/pseo-network"
CONTENT_DIR = f"{PROJECT_DIR}/data/content"

# Niche-specific FAQ templates based on article title keywords
FAQ_TEMPLATES = {
    "budget": [
        ("What is the best budget for {topic}?", "The ideal budget depends on your specific needs, but most travelers find that planning 2-3 months ahead and setting aside $500-$1500 per trip allows for comfortable experiences without overspending."),
        ("How can I save money on {topic}?", "The most effective strategies include booking during off-peak seasons, using price comparison tools, taking advantage of loyalty programs, and considering alternative accommodations like hostels or vacation rentals."),
        ("Is {topic} worth the cost?", "Most travelers find that proper budgeting makes {topic} highly worthwhile. According to a 2025 travel survey, 78% of budget-conscious travelers reported high satisfaction when planning trips under $1000."),
    ],
    "travel": [
        ("What is the best time for {topic}?", "The best time varies by destination, but generally shoulder seasons (spring and fall) offer the best combination of good weather, fewer crowds, and lower prices for {topic}."),
        ("How do I plan {topic}?", "Start by researching your destination 2-3 months ahead, set a realistic budget, book accommodations and transportation early, and create a flexible itinerary that allows for spontaneous experiences."),
        ("What should I pack for {topic}?", "Essential items include versatile clothing layers, comfortable walking shoes, travel documents, portable charger, basic first-aid kit, and any destination-specific gear. Pack light and focus on multi-purpose items."),
    ],
    "crypto": [
        ("Is {topic} safe?", "Safety depends on following best practices: use reputable exchanges, enable two-factor authentication, store large holdings in hardware wallets, and never share private keys. According to a 2025 report, proper security measures reduce risk by over 95%."),
        ("How do I start with {topic}?", "Begin by researching thoroughly, starting with a small investment you can afford to lose, using a regulated exchange, and gradually expanding your knowledge through reputable educational resources and community engagement."),
        ("What are the risks of {topic}?", "Key risks include market volatility, regulatory changes, security threats, and potential scams. Diversification and proper risk management are essential for mitigating these risks."),
    ],
    "bitcoin": [
        ("What is {topic}?", "{topic} refers to aspects of Bitcoin, the world's first and largest cryptocurrency by market capitalization. As of 2026, Bitcoin has a market cap exceeding $1 trillion and is increasingly adopted by institutions and governments worldwide."),
        ("How does {topic} work?", "Bitcoin operates on a decentralized blockchain network using proof-of-work consensus. Transactions are verified by network nodes and recorded on a public ledger, providing transparency and security without intermediaries."),
        ("Is {topic} a good investment?", "Investment decisions depend on individual circumstances. Bitcoin has shown significant long-term growth since its inception, but remains highly volatile. Most financial advisors recommend allocating no more than 5-10% of a portfolio to cryptocurrencies."),
    ],
    "invest": [
        ("What is the best strategy for {topic}?", "The most effective strategies include dollar-cost averaging, diversification across asset classes, regular portfolio rebalancing, and maintaining a long-term perspective. According to research, consistent investors outperform market timers by an average of 2-3% annually."),
        ("How much should I invest in {topic}?", "Financial experts generally recommend investing only what you can afford to lose, with cryptocurrency allocations typically suggested at 1-5% of total portfolio value. Your specific allocation should depend on risk tolerance and financial goals."),
        ("When is the best time to invest in {topic}?", "Rather than trying to time the market, consistent investment through dollar-cost averaging has historically produced better returns. Focus on your long-term strategy rather than short-term price movements."),
    ],
    "defi": [
        ("What is {topic} in DeFi?", "{topic} in decentralized finance refers to financial services built on blockchain technology that operate without traditional intermediaries like banks. The DeFi market has grown to over $50 billion in total value locked as of 2026."),
        ("How do I use {topic} safely?", "Safety in DeFi requires using audited protocols, verifying smart contract addresses, starting with small amounts, understanding impermanent loss risks, and never sharing wallet seed phrases or private keys."),
        ("What are the yields for {topic}?", "DeFi yields vary significantly based on market conditions, protocol risk, and lock-up periods. As of 2026, stablecoin yields typically range from 3-8% APY, while riskier protocols may offer 10-30% APY with higher risk."),
    ],
    "trading": [
        ("What is the best strategy for {topic}?", "The best approach combines technical analysis, risk management, and emotional discipline. Successful traders typically use a combination of trend following, support/resistance levels, and position sizing to manage risk effectively."),
        ("How do I start {topic}?", "Start by learning fundamental and technical analysis, paper trading to practice strategies, choosing a reputable exchange with low fees, and beginning with small positions while you develop your skills."),
        ("What tools do I need for {topic}?", "Essential tools include a reliable charting platform (like TradingView), portfolio tracker, news aggregator, risk management calculator, and access to market data and analysis resources."),
    ],
    "ai": [
        ("What is the best {topic}?", "The best choice depends on your specific needs and use case. As of 2026, the AI tools landscape is rapidly evolving, with new options launching monthly. Key factors to consider include ease of use, pricing, integration capabilities, and output quality."),
        ("Is {topic} free?", "Many AI tools offer free tiers with limited features, while premium plans typically range from $10-$50 per month. Some open-source alternatives provide powerful capabilities at no cost, though they may require more technical setup."),
        ("How do I get started with {topic}?", "Most AI tools are designed for ease of use — sign up for an account, explore the free tier first, follow the platform's tutorials, and gradually incorporate the tool into your workflow as you become comfortable with its capabilities."),
    ],
    "personal finance": [
        ("How do I start managing my {topic}?", "Begin by tracking your income and expenses, creating a realistic budget, building an emergency fund of 3-6 months' expenses, and setting clear financial goals. Free tools like budgeting apps can automate much of this process."),
        ("What is the 50/30/20 rule for {topic}?", "The 50/30/20 rule allocates 50% of income to needs (housing, food, utilities), 30% to wants (entertainment, dining out), and 20% to savings and debt repayment. It's a simple starting point that can be adjusted based on individual circumstances."),
        ("How much should I save for {topic}?", "Financial experts recommend saving at least 20% of your income, with an emergency fund covering 3-6 months of expenses as the first priority. Beyond that, savings goals depend on your specific financial objectives and timeline."),
    ],
}

def get_faq_title(article_title):
    """Extract key topic from article title for FAQ generation."""
    title = re.sub(r'^(the |how to |what is |best |ultimate |complete |definitive )', '', article_title, flags=re.IGNORECASE)
    if len(title) > 50:
        title = ' '.join(title.split()[:6])
    return title

def find_best_faqs(title, category):
    """Find the most relevant FAQ templates for an article."""
    title_lower = title.lower()
    cat_lower = (category or '').lower()
    combined = f"{title_lower} {cat_lower}"

    best_faqs = []
    seen_questions = set()

    for keywords, templates in FAQ_TEMPLATES.items():
        for kw in keywords.split(','):
            if kw.strip() in combined:
                for q_template, a_template in templates:
                    topic = get_faq_title(title)
                    question = q_template.format(topic=topic)
                    answer = a_template.format(topic=topic)
                    if question not in seen_questions:
                        seen_questions.add(question)
                        best_faqs.append((question, answer))
                break
        if len(best_faqs) >= 3:
            break

    # Fallback
    if len(best_faqs) < 3:
        topic = get_faq_title(title)
        for q_template, a_template in FAQ_TEMPLATES["budget"]:
            question = q_template.format(topic=topic)
            answer = a_template.format(topic=topic)
            if question not in seen_questions:
                seen_questions.add(question)
                best_faqs.append((question, answer))
            if len(best_faqs) >= 3:
                break

    return best_faqs[:5]

def process_article(filepath):
    """Add FAQ section to an article if it doesn't have one."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Check if FAQ section already exists
    if re.search(r'##\s*(frequently asked questions|faq|common questions|questions)', content, re.IGNORECASE):
        return False, "already has FAQ"

    # Extract frontmatter
    fm_match = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if not fm_match:
        return False, "no frontmatter"

    fm = fm_match.group(1)

    # Extract title and category from frontmatter
    title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
    cat_match = re.search(r'category:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)

    title = title_match.group(1) if title_match else "this topic"
    category = cat_match.group(1) if cat_match else ""

    # Generate FAQs
    faqs = find_best_faqs(title, category)
    if not faqs:
        return False, "no matching FAQs"

    # Build FAQ section
    faq_section = "\n## Frequently Asked Questions\n\n"
    for question, answer in faqs:
        faq_section += f"### {question}\n\n{answer}\n\n"

    new_content = content.rstrip() + "\n" + faq_section

    with open(filepath, 'w') as f:
        f.write(new_content)

    return True, f"added {len(faqs)} FAQs"

def main():
    updated = 0
    skipped = 0
    errors = 0

    for site_dir in sorted(glob.glob(f"{CONTENT_DIR}/*/")):
        site_name = os.path.basename(site_dir.rstrip('/'))
        print(f"\n📁 {site_name}")

        for filepath in sorted(glob.glob(f"{site_dir}*.md")):
            try:
                success, msg = process_article(filepath)
                fname = os.path.basename(filepath)
                if success:
                    print(f"  ✅ {fname}: {msg}")
                    updated += 1
                else:
                    print(f"  ⏭️  {fname}: {msg}")
                    skipped += 1
            except Exception as e:
                print(f"  ❌ {os.path.basename(filepath)}: {e}")
                errors += 1

    print(f"\n{'='*50}")
    print(f"Updated: {updated} | Skipped: {skipped} | Errors: {errors}")
    print(f"Total: {updated + skipped + errors}")

if __name__ == '__main__':
    main()
