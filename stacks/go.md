# Go Stack

Selected when `Active stack: go` is set at the top of `../workflow.md`. Every role reads this file before starting work. Commands run from the project root (`work/`), after dependencies are installed, through the project-local environment.

## Environment
Go 1.21+; follow the go.mod directive. Keep caches in `work/`: `export GOPATH=$PWD/.cache/go GOMODCACHE=$PWD/.cache/go/mod GOBIN=$PWD/.cache/bin` (document in a script, ignore `.cache/`). Run `go mod download` and `go build ./...`.

## Testing
Standard testing in `*_test.go`: `go test ./...`; selection: `go test ./path -run TestName`; race detection where supported: `go test -race ./...`.

## Frameworks, Linting, and Supporting Tools
Testify, gomock, testcontainers, autogold, or rapid when justified; `go vet ./...` and `gofmt`.

## Role Application
Apply each role's Core Skills to this stack. Use framework-specific setup only when the architecture selects it. For automation, run integration/E2E tools appropriate to the product; code-level tests alone do not establish end-to-end acceptance. For manual QA, exercise the running service, CLI, or UI and record runtime and platform versions.

## Commands
| Install deps | Run tests | Lint / check |
| --- | --- | --- |
| `go mod download` | `go test ./...` | `go vet ./...`; `gofmt -l .` |

## Table-Driven Test Pattern
```go
func TestNormalize(t *testing.T) {
    cases := []struct { name, input, want string }{
        {name: "trim spaces", input: " x ", want: "x"},
        {name: "empty", input: "", want: ""},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            if got := Normalize(tc.input); got != tc.want {
                t.Fatalf("Normalize(%q) = %q; want %q", tc.input, got, tc.want)
            }
        })
    }
}
```
Illustrative structure: replace `Normalize` with the project's real API and import `testing`.

## Quality Checklist
- [ ] Runtime and dependency versions match the accepted environment.
- [ ] Commands exist in the target repository and pass, or blockers are reported.
- [ ] Relevant logic, integration boundaries, and failure behavior have evidence.
