"""Exercise real failure detection without changing the delivered definitions."""
from pathlib import Path
import shutil
import tempfile
import unittest
from validate import validate

ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ('agents', 'adapters'):
            shutil.copytree(ROOT / name, self.root / name)
        for name in ('AGENTS.md', 'README.md', 'workflow.md'):
            shutil.copy2(ROOT / name, self.root / name)
        (self.root / 'work').mkdir(parents=True)
        (self.root / 'description').mkdir()

    def edit(self, relative, old, new):
        path = self.root / relative
        path.write_text(path.read_text().replace(old, new))

    def test_valid_framework(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_role(self):
        (self.root / 'agents/devops/SKILL.md').unlink()
        self.assertTrue(any('devops/SKILL.md: missing' in e for e in validate(self.root)))

    def test_invalid_metadata(self):
        self.edit('agents/reviewer/SKILL.md', 'name: reviewer-skills', 'name: wrong')
        self.assertTrue(any('invalid or duplicate name' in e for e in validate(self.root)))

    def test_missing_stack(self):
        self.edit('agents/engineer/SKILL.md', '## Go Stack', '## Removed Stack')
        self.assertTrue(any('missing Go Stack' in e for e in validate(self.root)))

    def test_nonportable_reference(self):
        self.edit('agents/architect/instructions.md', '../../workflow.md', '/home/user/workflow.md')
        self.assertTrue(any('nonportable reference' in e for e in validate(self.root)))

    def test_instruction_limit(self):
        path = self.root / 'agents/qa-manual/instructions.md'
        path.write_text(path.read_text() + '\n' * 101)
        self.assertTrue(any('exceeds 100 lines' in e for e in validate(self.root)))

    def test_missing_completion_gate(self):
        self.edit('workflow.md', 'work done', 'removed command')
        self.assertTrue(any('missing contract work done' in e for e in validate(self.root)))

    def test_broken_canonical_reference(self):
        self.edit('agents/orchestrator/instructions.md', '../../workflow.md', '../../missing/workflow.md')
        self.assertTrue(any('unresolved reference' in e for e in validate(self.root)))


if __name__ == '__main__':
    unittest.main()
