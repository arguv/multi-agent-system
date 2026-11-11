"""Validate the portable team definition without third-party dependencies."""
from pathlib import Path
import re
import sys

ROLES = ('orchestrator', 'architect', 'devops', 'engineer', 'test-engineer',
         'reviewer', 'qa-automation', 'qa-manual')
HEADINGS = ('Role Overview', 'When This Role Activates', 'Inputs', 'Outputs',
            'Success Criteria', 'Loop-Back Handling', 'References')


def validate(root):
    errors = []
    names = set()
    for role in ROLES:
        for filename in ('instructions.md', 'SKILL.md'):
            path = root / 'agents' / role / filename
            label = path.relative_to(root).as_posix()
            if not path.is_file():
                errors.append(f'{label}: missing')
                continue
            content = path.read_text()
            front = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
            if not front:
                errors.append(f'{label}: missing frontmatter')
            else:
                fields = dict(re.findall(r'^(name|description): (.+)$', front[1], re.M))
                expected = role + ('-skills' if filename == 'SKILL.md' else '')
                if fields.get('name') != expected or expected in names:
                    errors.append(f'{label}: invalid or duplicate name')
                names.add(expected)
                desc = fields.get('description', '')
                if not (desc.startswith('"') and desc.endswith('"') and 'Use when' in desc):
                    errors.append(f'{label}: missing quoted description or activation trigger')
            if filename == 'instructions.md':
                if len(content.splitlines()) > 100:
                    errors.append(f'{label}: exceeds 100 lines')
                for heading in HEADINGS:
                    if f'## {heading}\n' not in content:
                        errors.append(f'{label}: missing {heading}')
                if 'SKILL.md' not in content or 'Before Any Work' not in content:
                    errors.append(f'{label}: missing pre-work requirement')
                if re.search(r'PHPUnit|pytest|go mod|Vitest|Jest|composer install', content):
                    errors.append(f'{label}: stack command in stable instructions')
            else:
                for heading in ('Core Skills (stack-independent)', 'PHP Stack', 'Python Stack',
                                'Go Stack', 'JS/TS Stack', 'Tooling Commands (quick reference)',
                                'Quality Checklist (all stacks)'):
                    if f'## {heading}\n' not in content:
                        errors.append(f'{label}: missing {heading}')
                for token in ('PHPUnit', 'pytest', 'Testify', 'Vitest', 'Jest', 'Table-Driven Test Pattern'):
                    if token not in content:
                        errors.append(f'{label}: missing {token}')
            for target in re.findall(r'`((?:\.\./)+(?:[^`]+))`', content):
                # Check canonical references, not example runtime artifacts or future reports.
                if target.endswith(('workflow.md', 'instructions.md', 'SKILL.md')):
                    if not (path.parent / target).is_file():
                        errors.append(f'{label}: unresolved reference {target}')
    required = ('AGENTS.md', 'README.md', 'workflow.md', 'adapters/codex.md',
                'adapters/claude-code.md', 'adapters/copilot.md', 'adapters/deepseek.md')
    for name in required:
        if not (root / name).is_file():
            errors.append(f'{name}: missing')
    workflow = root / 'workflow.md'
    if workflow.exists():
        content = workflow.read_text()
        for token in ('work start', 'work done', 'Loop-back ownership', 'Cleanup contract',
                      'description/manual-qa/results/report.md', 'description/<role>.md',
                      'description/environment.md', 'description/review.md', 'description/reports/automation.md'):
            if token not in content:
                errors.append(f'workflow.md: missing contract {token}')
    for folder in ('agents', 'adapters'):
        for path in (root / folder).rglob('*.md'):
            content = path.read_text()
            if re.search(r'(?:/home/|/Users/|[A-Z]:\\|plugin://|app://)', content):
                errors.append(f'{path.relative_to(root)}: nonportable reference')
    # Output directories are optional before a task starts; never create task outputs here.
    documents = [root / name for name in ('README.md', 'AGENTS.md', 'workflow.md')]
    documents += list((root / 'agents').rglob('*.md'))
    documents += list((root / 'adapters').glob('*.md'))
    stale_reports = re.compile(
        r'work/(?:delivery(?:/|\b)|(?:task|status|handoffs|architecture|environment|'
        r'implementation|change-set|test-plan|review|closure)\.md|reports/|'
        r'manual-qa/(?:plan\.md|results/))')
    for path in documents:
        if not path.is_file():
            continue
        content = path.read_text()
        label = path.relative_to(root).as_posix()
        if stale_reports.search(content):
            errors.append(f'{label}: obsolete project/report layout')
        project_path = '../../work/' if path.parent.parent.name == 'agents' else (
            '../work/' if path.parent.name == 'adapters' else 'work/')
        report_path = project_path.replace('work/', 'description/')
        if project_path not in content or report_path not in content:
            errors.append(f'{label}: missing project/report folder contract')
    for path in (root / 'work', root / 'description'):
        if path.exists() and not path.is_dir():
            errors.append(f'{path.relative_to(root)}: output path must be a directory')
    return errors


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print('PASS: 8 role pairs; metadata, instruction limits, 4 stacks, references, workflow contracts, and project/report folder layout')
