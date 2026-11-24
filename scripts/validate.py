"""Validate the portable team definition without third-party dependencies."""
from pathlib import Path
import re
import sys

ROLES = ('orchestrator', 'architect', 'devops', 'engineer', 'test-engineer',
         'reviewer', 'qa-automation', 'qa-manual')
STACKS = ('php', 'python', 'go', 'js-ts')
HEADINGS = ('Role Overview', 'Before Any Work', 'Core Skills', 'When This Role Activates',
            'Inputs', 'Outputs', 'Success Criteria', 'Loop-Back Handling',
            'Quality Checklist', 'References')
STACK_HEADINGS = ('Environment', 'Testing', 'Frameworks, Linting, and Supporting Tools',
                  'Commands', 'Quality Checklist')
STACK_RULE = 'stacks/<Active stack>.md'
COMMANDS = ('start work', 'finish work')
OLD_COMMANDS = re.compile(r'\bwork start\b|\bwork done\b')
REPORTS = ('01_requirements.md', '02_project_plan.md', '03_architecture_plan.md',
           '04_environment.md', '05_engineer_report.md', '06_test_report.md',
           '07_review_report.md', '08_qa_automation_report.md', '09_manual_qa_report.md')
ROLE_REPORT = {'orchestrator': '02_project_plan.md', 'architect': '03_architecture_plan.md',
               'devops': '04_environment.md', 'engineer': '05_engineer_report.md',
               'test-engineer': '06_test_report.md', 'reviewer': '07_review_report.md',
               'qa-automation': '08_qa_automation_report.md', 'qa-manual': '09_manual_qa_report.md'}
MAX_ROLE_LINES = 100
STACK_TOOL_WORDS = r'PHPUnit|pytest|go mod|Vitest|Jest|composer install|npm ci|Testify'


def check_roles(root, errors):
    agents = root / 'agents'
    expected = {f'{role}.md' for role in ROLES}
    if agents.is_dir():
        for entry in sorted(agents.iterdir()):
            if entry.name.startswith('.'):
                continue  # runner tool-state such as .claude/
            if entry.is_dir():
                errors.append(f'agents/{entry.name}: legacy role directory; use flat agents/<role>.md')
            elif entry.name not in expected:
                errors.append(f'agents/{entry.name}: unexpected file; agents/ holds exactly 8 role files')
    for role in ROLES:
        path = agents / f'{role}.md'
        label = f'agents/{role}.md'
        if not path.is_file():
            errors.append(f'{label}: missing')
            continue
        content = path.read_text()
        front = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
        if not front:
            errors.append(f'{label}: missing frontmatter')
        else:
            fields = dict(re.findall(r'^(name|description): (.+)$', front[1], re.M))
            if fields.get('name') != role:
                errors.append(f'{label}: invalid or duplicate name')
            desc = fields.get('description', '')
            if not (desc.startswith('"') and desc.endswith('"') and 'Use when' in desc):
                errors.append(f'{label}: missing quoted description or activation trigger')
        if len(content.splitlines()) > MAX_ROLE_LINES:
            errors.append(f'{label}: exceeds {MAX_ROLE_LINES} lines')
        for heading in HEADINGS:
            if f'## {heading}\n' not in content:
                errors.append(f'{label}: missing {heading}')
        if STACK_RULE not in content or 'Before starting work, read' not in content:
            errors.append(f'{label}: missing active stack rule ({STACK_RULE})')
        if re.search(STACK_TOOL_WORDS, content):
            errors.append(f'{label}: stack command in stable role file')
        if ROLE_REPORT[role] not in content:
            errors.append(f'{label}: missing own report {ROLE_REPORT[role]}')
        if 'SKILL.md' in content or 'instructions.md' in content:
            errors.append(f'{label}: legacy instructions/SKILL reference')
        if '../workflow.md' in content and not (path.parent / '../workflow.md').is_file():
            errors.append(f'{label}: unresolved reference ../workflow.md')


def check_stacks(root, errors):
    for name in STACKS:
        path = root / 'stacks' / f'{name}.md'
        label = f'stacks/{name}.md'
        if not path.is_file():
            errors.append(f'{label}: missing')
            continue
        content = path.read_text()
        for heading in STACK_HEADINGS:
            if f'## {heading}\n' not in content:
                errors.append(f'{label}: missing {heading}')
    workflow = root / 'workflow.md'
    if not workflow.is_file():
        return
    lines = [line for line in workflow.read_text().splitlines() if line.strip()]
    first = lines[0] if lines else ''
    match = re.fullmatch(r'Active stack: ([a-z0-9-]+)', first)
    if not match:
        errors.append('workflow.md: first line must be "Active stack: <name>"')
    elif not (root / 'stacks' / f'{match[1]}.md').is_file():
        errors.append(f'workflow.md: Active stack "{match[1]}" has no file stacks/{match[1]}.md')
    if sum(1 for line in workflow.read_text().splitlines() if line.startswith('Active stack:')) > 1:
        errors.append('workflow.md: multiple Active stack lines')


def check_workflow(root, errors):
    workflow = root / 'workflow.md'
    if not workflow.is_file():
        return
    content = workflow.read_text()
    for token in (*COMMANDS, *REPORTS, 'Loop-back ownership', 'Cleanup contract', STACK_RULE):
        if token not in content:
            errors.append(f'workflow.md: missing contract {token}')
    cleanup = re.search(r'## Cleanup contract\n(.*?)(?=\n## |\Z)', content, re.S)
    text = cleanup[1] if cleanup else ''
    if 'finish work' not in text or 'work/' not in text or 'description/' not in text \
            or 'empty' not in text:
        errors.append('workflow.md: cleanup contract must empty work/ and description/ on finish work')


def check_documents(root, errors):
    required = ('AGENTS.md', 'README.md', 'workflow.md', 'adapters/codex.md',
                'adapters/claude-code.md', 'adapters/copilot.md', 'adapters/deepseek.md')
    for name in required:
        if not (root / name).is_file():
            errors.append(f'{name}: missing')
    documents = [root / name for name in ('README.md', 'AGENTS.md', 'workflow.md')]
    documents += sorted((root / 'agents').glob('*.md')) + sorted((root / 'adapters').glob('*.md'))
    documents += sorted((root / 'stacks').glob('*.md'))
    stale = re.compile(
        r'work/(?:delivery(?:/|\b)|(?:task|status|handoffs|architecture|environment|'
        r'implementation|change-set|test-plan|review|closure)\.md|reports/|'
        r'manual-qa/(?:plan\.md|results/))|description/(?:task|status|handoffs|architecture|'
        r'environment|implementation|change-set|test-plan|review|orchestrator|architect|devops|'
        r'engineer|test-engineer|reviewer|qa-automation|qa-manual)\.md|description/reports/|'
        r'description/manual-qa/')
    for path in documents:
        if not path.is_file():
            continue
        content = path.read_text()
        label = path.relative_to(root).as_posix()
        if re.search(r'(?:/home/|/Users/|[A-Z]:\\|plugin://|app://)', content):
            errors.append(f'{label}: nonportable reference')
        if OLD_COMMANDS.search(content):
            errors.append(f'{label}: obsolete command (use start work / finish work)')
        if stale.search(content):
            errors.append(f'{label}: obsolete project/report layout')
        if path.parent == root / 'stacks':
            continue
        if path.parent.name in ('agents', 'adapters'):
            project_path = '../work/'
        else:
            project_path = 'work/'
        report_path = project_path.replace('work/', 'description/')
        if project_path not in content or report_path not in content:
            errors.append(f'{label}: missing project/report folder contract')
    for name in ('AGENTS.md', 'README.md'):
        path = root / name
        if path.is_file():
            content = path.read_text()
            for command in COMMANDS:
                if command not in content:
                    errors.append(f'{name}: missing command {command}')
            for report in REPORTS:
                if report not in content:
                    errors.append(f'{name}: missing report {report}')
    readme = root / 'README.md'
    if readme.is_file() and 'Active stack:' not in readme.read_text():
        errors.append('README.md: missing Active stack switching section')
    for path in (root / 'work', root / 'description'):
        if path.exists() and not path.is_dir():
            errors.append(f'{path.relative_to(root)}: output path must be a directory')


def validate(root):
    errors = []
    check_roles(root, errors)
    check_stacks(root, errors)
    check_workflow(root, errors)
    check_documents(root, errors)
    return errors


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print('PASS: 8 flat role files; Active stack and 4 stack files; start work / finish work; '
          'numbered reports 01-09; references and project/report folder layout')
