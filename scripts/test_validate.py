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
        for name in ('agents', 'adapters', 'stacks'):
            shutil.copytree(ROOT / name, self.root / name,
                            ignore=shutil.ignore_patterns('.*'))
        for name in ('AGENTS.md', 'README.md', 'workflow.md'):
            shutil.copy2(ROOT / name, self.root / name)
        (self.root / 'work').mkdir(parents=True)
        (self.root / 'description').mkdir()

    def edit(self, relative, old, new):
        path = self.root / relative
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new))

    def errors(self):
        return validate(self.root)

    def assertError(self, fragment):
        self.assertTrue(any(fragment in e for e in self.errors()), self.errors())

    # --- baseline -------------------------------------------------------
    def test_valid_framework(self):
        self.assertEqual(self.errors(), [])

    def test_real_repository_is_valid(self):
        self.assertEqual(validate(ROOT), [])

    # --- role structure -------------------------------------------------
    def test_exactly_eight_flat_role_files(self):
        files = sorted(p.name for p in (self.root / 'agents').iterdir())
        self.assertEqual(len(files), 8)
        self.assertTrue(all(f.endswith('.md') for f in files))

    def test_missing_role(self):
        (self.root / 'agents/devops.md').unlink()
        self.assertError('agents/devops.md: missing')

    def test_legacy_role_directory_rejected(self):
        legacy = self.root / 'agents/engineer'
        legacy.mkdir()
        (legacy / 'instructions.md').write_text('legacy')
        self.assertError('legacy role directory')

    def test_unexpected_agent_file_rejected(self):
        (self.root / 'agents/extra.md').write_text('# extra')
        self.assertError('unexpected file')

    def test_invalid_metadata(self):
        self.edit('agents/reviewer.md', 'name: reviewer', 'name: wrong')
        self.assertError('invalid or duplicate name')

    def test_missing_activation_trigger(self):
        self.edit('agents/architect.md', 'Use when', 'Used for')
        self.assertError('missing quoted description or activation trigger')

    def test_missing_heading(self):
        self.edit('agents/qa-manual.md', '## Loop-Back Handling\n', '## Something Else\n')
        self.assertError('missing Loop-Back Handling')

    def test_role_line_limit(self):
        path = self.root / 'agents/qa-manual.md'
        path.write_text(path.read_text() + '\n' * 101)
        self.assertError('exceeds 100 lines')

    def test_stack_command_in_role_rejected(self):
        path = self.root / 'agents/engineer.md'
        path.write_text(path.read_text() + '\nRun PHPUnit now.\n')
        self.assertError('stack command in stable role file')

    def test_missing_own_report(self):
        self.edit('agents/devops.md', '04_environment.md', '04_other.md')
        self.assertError('missing own report 04_environment.md')

    def test_legacy_instruction_reference_rejected(self):
        path = self.root / 'agents/architect.md'
        path.write_text(path.read_text() + '\nSee `SKILL.md`.\n')
        self.assertError('legacy instructions/SKILL reference')

    # --- active stack ---------------------------------------------------
    def test_active_stack_rule_required_in_every_role(self):
        for role in ('architect', 'engineer', 'test-engineer'):
            with self.subTest(role=role):
                path = self.root / f'agents/{role}.md'
                original = path.read_text()
                path.write_text(original.replace('stacks/<Active stack>.md', 'stacks/php.md'))
                self.assertError(f'agents/{role}.md: missing active stack rule')
                path.write_text(original)

    def test_active_stack_must_exist(self):
        self.edit('workflow.md', 'Active stack: php', 'Active stack: cobol')
        self.assertError('Active stack "cobol" has no file stacks/cobol.md')

    def test_active_stack_line_must_be_first(self):
        path = self.root / 'workflow.md'
        path.write_text('# Title\n\n' + path.read_text())
        self.assertError('first line must be "Active stack: <name>"')

    def test_switching_to_each_stack_is_valid(self):
        for name in ('python', 'go', 'js-ts', 'php'):
            with self.subTest(stack=name):
                path = self.root / 'workflow.md'
                lines = path.read_text().splitlines()
                lines[0] = f'Active stack: {name}'
                path.write_text('\n'.join(lines) + '\n')
                self.assertEqual(self.errors(), [])

    def test_missing_stack_file(self):
        (self.root / 'stacks/go.md').unlink()
        self.assertError('stacks/go.md: missing')

    def test_stack_missing_section(self):
        self.edit('stacks/python.md', '## Testing\n', '## Other\n')
        self.assertError('stacks/python.md: missing Testing')

    def test_multiple_active_stack_lines(self):
        path = self.root / 'workflow.md'
        path.write_text(path.read_text() + '\nActive stack: python\n')
        self.assertError('multiple Active stack lines')

    # --- commands -------------------------------------------------------
    def test_missing_finish_work_contract(self):
        self.edit('workflow.md', 'finish work', 'removed command')
        self.assertError('missing contract finish work')

    def test_missing_start_work_contract(self):
        self.edit('workflow.md', 'start work', 'removed command')
        self.assertError('missing contract start work')

    def test_old_command_rejected(self):
        for name in ('AGENTS.md', 'README.md', 'workflow.md', 'agents/engineer.md', 'adapters/codex.md'):
            with self.subTest(file=name):
                path = self.root / name
                original = path.read_text()
                path.write_text(original + '\nSend work start to begin.\n')
                self.assertError('obsolete command')
                path.write_text(original + '\nSend work done to end.\n')
                self.assertError('obsolete command')
                path.write_text(original)

    def test_readme_must_document_commands(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text().replace('finish work', 'the end command'))
        self.assertError('README.md: missing command finish work')

    def test_cleanup_contract_must_empty_both_folders(self):
        self.edit('workflow.md', 'remove the contents of `work/` and `description/` only',
                  'do nothing about outputs')
        self.assertError('cleanup contract must empty work/ and description/')

    # --- numbered reports -----------------------------------------------
    def test_numbered_reports_required_in_workflow(self):
        path = self.root / 'workflow.md'
        path.write_text(path.read_text().replace('07_review_report.md', 'review.md'))
        self.assertError('missing contract 07_review_report.md')

    def test_legacy_report_path_rejected(self):
        self.edit('agents/reviewer.md', '../description/07_review_report.md',
                  '../description/review.md')
        self.assertError('obsolete project/report layout')

    def test_legacy_staging_path_rejected(self):
        self.edit('agents/engineer.md', '../work/`, preserving', '../work/delivery/`, preserving')
        self.assertError('obsolete project/report layout')

    def test_readme_lists_all_reports(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text().replace('09_manual_qa_report.md', 'x.md'))
        self.assertError('README.md: missing report 09_manual_qa_report.md')

    # --- portability and output folders --------------------------------
    def test_nonportable_reference(self):
        self.edit('agents/architect.md', '../workflow.md', '/home/user/workflow.md')
        self.assertError('nonportable reference')

    def test_adapter_requires_folder_contract(self):
        self.edit('adapters/codex.md', '../description/', '../missing/')
        self.assertError('missing project/report folder contract')

    def test_missing_output_directories_are_valid_before_start(self):
        (self.root / 'work').rmdir()
        (self.root / 'description').rmdir()
        self.assertEqual(self.errors(), [])
        self.assertFalse((self.root / 'work').exists())
        self.assertFalse((self.root / 'description').exists())

    def test_validation_leaves_output_folders_empty(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(list((self.root / 'work').iterdir()), [])
        self.assertEqual(list((self.root / 'description').iterdir()), [])

    def test_repository_output_folders_are_empty(self):
        for name in ('work', 'description'):
            path = ROOT / name
            if path.exists():
                self.assertEqual(list(path.iterdir()), [], name)


if __name__ == '__main__':
    unittest.main()
