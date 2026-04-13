---
name: Compiler Internals
description: "LLVM and GCC compiler internals. Custom optimization passes, IR manipulation, code generation, ISA-aware optimization, and compiler toolchain development."
category: low-level
tags: llvm, gcc, compiler, ir, optimization, codegen, passes, clang, isa
---

# Compiler Internals

Expert in compiler infrastructure — understanding and extending LLVM/GCC for custom optimization, code generation, and analysis.

## Use this skill when

- Writing custom LLVM or GCC optimization passes
- Understanding compiler IR (LLVM IR, GIMPLE, RTL)
- Analyzing generated assembly for performance bottlenecks
- Implementing domain-specific code generation
- Writing static analysis tools using Clang AST / LibTooling
- Building custom sanitizers or instrumentation
- Understanding auto-vectorization, loop unrolling, and inlining decisions

## LLVM Architecture Overview

```
Source Code (.c/.cpp)
    │
    ▼ (Clang Frontend)
Clang AST → Semantic Analysis → LLVM IR (.ll)
    │
    ▼ (LLVM Middle-End Optimizer)
LLVM IR → Transform Passes → Optimized LLVM IR
    │
    ▼ (LLVM Backend)
SelectionDAG / GlobalISel → MachineIR → MCInst → Assembly/Object
```

### IR Hierarchy

| Level | Representation | Use For |
|---|---|---|
| **Clang AST** | Source-level tree | Refactoring, linting, semantic analysis |
| **LLVM IR** | SSA-form, typed, target-independent | Optimization passes, analysis |
| **MachineIR** | Target-specific, virtual registers | Instruction selection, register allocation |
| **MCInst** | Final instructions | Encoding, assembly emission |

## Writing an LLVM Pass (New Pass Manager)

```cpp
// MyPass.h — A function pass that counts instructions
#include "llvm/IR/PassManager.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"

namespace llvm {

class MyCountPass : public PassInfoMixin<MyCountPass> {
public:
    PreservedAnalyses run(Function &F, FunctionAnalysisManager &AM) {
        unsigned count = 0;
        for (auto &BB : F)
            for (auto &I : BB)
                ++count;
        errs() << F.getName() << ": " << count << " instructions\n";
        return PreservedAnalyses::all();  // We don't modify IR
    }
};

} // namespace llvm
```

### Registering the Pass

```cpp
// Plugin registration for opt
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Passes/PassBuilder.h"

llvm::PassPluginLibraryInfo getMyPluginInfo() {
    return {LLVM_PLUGIN_API_VERSION, "MyPlugin", LLVM_VERSION_STRING,
        [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM, ...) {
                    if (Name == "my-count") {
                        FPM.addPass(MyCountPass());
                        return true;
                    }
                    return false;
                });
        }};
}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() { return getMyPluginInfo(); }
```

```bash
# Build and run
cmake -DLLVM_DIR=/path/to/llvm/lib/cmake/llvm ..
make
opt -load-pass-plugin=./libMyPlugin.so -passes=my-count input.ll -o /dev/null
```

## LLVM IR Manipulation

```cpp
// Creating instructions programmatically
IRBuilder<> Builder(BB);  // Insert at end of BasicBlock

// Allocate an i32 on the stack
AllocaInst *Alloca = Builder.CreateAlloca(Type::getInt32Ty(Ctx), nullptr, "x");

// Store a constant
Builder.CreateStore(ConstantInt::get(Type::getInt32Ty(Ctx), 42), Alloca);

// Load and add
Value *Load = Builder.CreateLoad(Type::getInt32Ty(Ctx), Alloca);
Value *Sum = Builder.CreateAdd(Load, ConstantInt::get(Type::getInt32Ty(Ctx), 1));

// Conditional branch
Value *Cmp = Builder.CreateICmpSGT(Sum, ConstantInt::get(Type::getInt32Ty(Ctx), 0));
Builder.CreateCondBr(Cmp, TrueBB, FalseBB);
```

## Clang AST Analysis (LibTooling)

```cpp
// Find all function calls in source code
class CallFinder : public RecursiveASTVisitor<CallFinder> {
public:
    bool VisitCallExpr(CallExpr *CE) {
        if (auto *FD = CE->getDirectCallee()) {
            llvm::outs() << "Call to: " << FD->getName() << "\n";
        }
        return true;
    }
};

// Use with ClangTool
class MyAction : public ASTFrontendAction {
    std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI,
                                                    StringRef File) override {
        return std::make_unique<MyConsumer>();
    }
};

int main(int argc, const char **argv) {
    auto DB = FixedCompilationDatabase::loadFromCommandLine(argc, argv, Err);
    ClangTool Tool(*DB, Sources);
    return Tool.run(newFrontendActionFactory<MyAction>().get());
}
```

## Compiler Optimization Insights

### Understanding Optimization Reports

```bash
# Clang optimization remarks
clang -O2 -Rpass=loop-vectorize -Rpass-missed=loop-vectorize \
      -Rpass-analysis=loop-vectorize -fsave-optimization-record file.c

# GCC optimization reports
gcc -O2 -fopt-info-vec-all file.c           # Vectorization info
gcc -O2 -fopt-info-inline-all file.c        # Inlining decisions
gcc -O2 -fdump-tree-all -fdump-ipa-all file.c  # Dump all IR stages
```

### Key Passes & What They Do

| Pass | Effect | When It Matters |
|---|---|---|
| `instcombine` | Algebraic simplification | Always |
| `mem2reg` | Stack → SSA registers | First pass, essential |
| `inline` | Function inlining | Hot paths |
| `loop-vectorize` | SIMD vectorization | Numeric loops |
| `gvn` | Global value numbering | Redundant computation |
| `licm` | Loop-invariant code motion | Hoisting out of loops |
| `simplifycfg` | Dead block elimination | After other passes |
| `slp-vectorizer` | Straight-line vectorization | Adjacent operations |

### Inspecting Generated Code

```bash
# Emit LLVM IR
clang -S -emit-llvm -O2 file.c -o file.ll

# Emit optimized assembly with annotations
clang -S -O2 -fverbose-asm file.c -o file.s

# Compare optimization levels
diff <(clang -S -O0 -o - file.c) <(clang -S -O2 -o - file.c)

# Godbolt-style local exploration
clang -S -O2 -masm=intel file.c -o - | less
```

## Anti-Patterns

- ❌ Writing passes that modify IR but return `PreservedAnalyses::all()`
- ❌ Assuming specific IR shapes without checking (use pattern matching)
- ❌ Not running `opt -verify` after IR transformations
- ❌ Ignoring `undef` and `poison` semantics in LLVM IR
- ❌ Fighting the optimizer instead of writing optimization-friendly source
- ❌ Not using `-save-temps` to inspect IR at each stage
