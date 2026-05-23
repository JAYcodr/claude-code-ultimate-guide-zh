
#!/usr/bin/env python3
import yaml
import os
from deep_translator import GoogleTranslator

# Translation mapping for specific technical terms
term_map = {
    "Agent": "智能体",
    "Skill": "技能",
    "Command": "命令",
    "Hook": "钩子",
    "Workflow": "工作流",
    "MCP": "MCP",
    "Context": "上下文",
    "Memory": "记忆"
}

# Initialize translator
translator = GoogleTranslator(source='en', target='zh-CN')

def translate_text(text: str) -> str:
    if not text:
        return text
    # Use translator for general text
    result = translator.translate(text)
    # Replace technical terms with consistent translations
    for en, zh in term_map.items():
        result = result.replace(en, zh)
        # Also check lowercase and plural
        result = result.replace(en.lower(), zh)
        if en.endswith('y'):
            result = result.replace(en[:-1] + 'ies', zh)
        else:
            result = result.replace(en + 's', zh)
    return result

def translate_question_file(file_path: str):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Translate category
    data['category'] = translate_text(data['category'])
    
    # Translate each question
    for q in data.get('questions', []):
        q['question'] = translate_text(q['question'])
        # Translate options
        for key in ['a', 'b', 'c', 'd']:
            if key in q.get('options', {}):
                q['options'][key] = translate_text(q['options'][key])
        # Translate explanation
        if 'explanation' in q:
            q['explanation'] = translate_text(q['explanation'])
        # Translate doc_reference section name
        if 'doc_reference' in q and 'section' in q['doc_reference']:
            q['doc_reference']['section'] = translate_text(q['doc_reference']['section'])
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def main():
    questions_dir = '/workspace/quiz/questions'
    files = [
        '01-quick-start.yaml',
        '02-core-concepts.yaml',
        '03-memory-settings.yaml',
        '04-agents.yaml',
        '05-skills.yaml',
        '06-commands.yaml',
        '07-hooks.yaml',
        '08-mcp-servers.yaml',
        '09-advanced-patterns.yaml',
        '10-reference.yaml',
        '11-learning-with-ai.yaml',
        '12-architecture.yaml',
        '13-security.yaml',
        '14-privacy-observability.yaml',
        '15-ai-ecosystem.yaml',
        '16-team-metrics.yaml'
    ]
    for file in files:
        translate_question_file(os.path.join(questions_dir, file))
    print("Done!")

if __name__ == "__main__":
    main()

