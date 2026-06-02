#!/usr/bin/env python3
"""
STATE.yaml Agent Coordinator
Reads/writes STATE.yaml for autonomous multi-agent coordination.

Usage:
  python state-coordinator.py claim <agent-name> <task-description>
  python state-coordinator.py complete <agent-name> <result-summary>
  python state-coordinator.py status
  python state-coordinator.py next-task <agent-name>
"""

import sys
import os
import yaml
import json
from datetime import datetime
from pathlib import Path

STATE_PATH = Path(__file__).parent / "STATE.yaml"

def load_state():
    """Load STATE.yaml, return dict."""
    with open(STATE_PATH, 'r') as f:
        return yaml.safe_load(f)

def save_state(state):
    """Save STATE.yaml atomically."""
    state['project']['last_activity'] = datetime.now().strftime('%Y-%m-%d')
    tmp_path = STATE_PATH.with_suffix('.tmp')
    with open(tmp_path, 'w') as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    os.replace(tmp_path, STATE_PATH)

def claim_task(agent_name, task_description):
    """Agent claims a task."""
    state = load_state()
    if agent_name not in state.get('agents', {}):
        print(f"ERROR: Agent '{agent_name}' not found in STATE.yaml")
        print(f"Available agents: {list(state.get('agents', {}).keys())}")
        return False

    agent = state['agents'][agent_name]
    if agent['status'] == 'working':
        print(f"WARNING: {agent_name} already working on: {agent['current_task']}")
        return False

    agent['status'] = 'working'
    agent['current_task'] = task_description
    save_state(state)
    print(f"✅ {agent_name} claimed: {task_description}")
    return True

def complete_task(agent_name, result_summary):
    """Agent completes current task."""
    state = load_state()
    if agent_name not in state.get('agents', {}):
        print(f"ERROR: Agent '{agent_name}' not found in STATE.yaml")
        return False

    agent = state['agents'][agent_name]
    if agent['status'] != 'working':
        print(f"WARNING: {agent_name} is not currently working on anything")
        return False

    task = agent.get('current_task', 'unknown')
    agent['status'] = 'idle'
    agent['current_task'] = None
    agent['last_completed'] = {
        'task': task,
        'result': result_summary,
        'completed_at': datetime.now().isoformat()
    }
    save_state(state)
    print(f"✅ {agent_name} completed: {task}")
    print(f"   Result: {result_summary}")
    return True

def show_status():
    """Print current state summary."""
    state = load_state()
    
    print(f"📋 Project: {state['project']['name']}")
    print(f"   Phase: {state['project']['phase']} | Status: {state['project']['status']}")
    print(f"   Last Activity: {state['project']['last_activity']}")
    print()
    
    print("🌐 Sites:")
    for name, site in state.get('sites', {}).items():
        status_icon = "🟢" if site['status'] == 'active' else "🔴"
        print(f"   {status_icon} {name}: {site.get('articles', 0)}/{site.get('target', '?')} articles")
        if site.get('needs'):
            print(f"      Needs: {', '.join(site['needs'])}")
    print()
    
    print("🤖 Agents:")
    for name, agent in state.get('agents', {}).items():
        status_icon = "🟢" if agent['status'] == 'idle' else "🔧"
        task = f" → {agent['current_task']}" if agent.get('current_task') else ""
        print(f"   {status_icon} {name}: {agent['status']}{task}")
    print()
    
    print("🚧 Blockers:")
    for blocker in state.get('blockers', []):
        impact = blocker.get('impact', 'unknown')
        icon = "🔴" if impact == 'critical' else "🟡"
        print(f"   {icon} [{blocker['id']}] {blocker['description']}")
    print()
    
    print("📊 Metrics:")
    metrics = state.get('metrics', {})
    print(f"   Articles: {metrics.get('total_articles', '?')} | Pages: {metrics.get('total_pages', '?')}")
    print(f"   Revenue: {metrics.get('revenue', '?')}")

def get_next_task(agent_name):
    """Suggest next task for an agent based on current state."""
    state = load_state()
    
    if agent_name not in state.get('agents', {}):
        print(f"ERROR: Agent '{agent_name}' not found")
        return

    agent = state['agents'][agent_name]
    capabilities = agent.get('capabilities', [])
    
    # Check what needs doing based on capabilities
    suggestions = []
    
    # Content generation needed?
    if 'article-generation' in capabilities or 'content-burst' in capabilities:
        for name, site in state.get('sites', {}).items():
            current = site.get('articles', 0)
            target = site.get('target', 100)
            if current < target:
                suggestions.append(f"Generate content for {name} ({current}/{target})")
    
    # SEO work?
    if 'keyword-research' in capabilities:
        suggestions.append("Run keyword research for underperforming niches")
    
    # Deployment?
    if 'deploy' in capabilities:
        has_blockers = any(b.get('impact') == 'critical' for b in state.get('blockers', []))
        if has_blockers:
            suggestions.append("BLOCKED: Domains needed before deployment")
        else:
            suggestions.append("Deploy sites to Cloudflare Pages")
    
    if not suggestions:
        print(f"✅ {agent_name}: No tasks available — all caught up!")
    else:
        print(f"📋 Suggested tasks for {agent_name}:")
        for i, s in enumerate(suggestions, 1):
            print(f"   {i}. {s}")

def main():
    if len(sys.argv) < 2:
        print("Usage: state-coordinator.py [status|claim|complete|next-task]")
        print("  status                  Show current state")
        print("  claim <agent> <task>    Claim a task")
        print("  complete <agent> <msg>  Complete current task")
        print("  next-task <agent>       Get suggested next task")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'status':
        show_status()
    elif command == 'claim':
        if len(sys.argv) < 4:
            print("Usage: state-coordinator.py claim <agent-name> <task-description>")
            sys.exit(1)
        claim_task(sys.argv[2], ' '.join(sys.argv[3:]))
    elif command == 'complete':
        if len(sys.argv) < 4:
            print("Usage: state-coordinator.py complete <agent-name> <result>")
            sys.exit(1)
        complete_task(sys.argv[2], ' '.join(sys.argv[3:]))
    elif command == 'next-task':
        if len(sys.argv) < 3:
            print("Usage: state-coordinator.py next-task <agent-name>")
            sys.exit(1)
        get_next_task(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
