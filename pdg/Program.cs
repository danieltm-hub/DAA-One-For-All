using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.CodeAnalysis.FlowAnalysis;
using Microsoft.CodeAnalysis.Operations;
using System;
using System.Collections.Generic;
using System.Linq;

public class DependencyGraph
{
    // Maps an operation to the operations it depends on (correct direction)
    public Dictionary<IOperation, HashSet<IOperation>> Dependencies { get; } = new();

    public void AddDependency(IOperation dependent, IOperation dependency)
    {
        if (!Dependencies.ContainsKey(dependent))
            Dependencies[dependent] = new HashSet<IOperation>();
        Dependencies[dependent].Add(dependency);
    }

    public void AddNode(IOperation node)
    {
        if (!Dependencies.ContainsKey(node))
            Dependencies[node] = new HashSet<IOperation>();
    }
}

public class DependencyGraphBuilder
{
    public DependencyGraph Build(SemanticModel semanticModel, MethodDeclarationSyntax method)
    {
        var cfg = ControlFlowGraph.Create(method, semanticModel);
        var graph = new DependencyGraph();

        var lastWrite = new Dictionary<ISymbol, IOperation>();
        var previousInBlock = new Dictionary<IOperation, IOperation>();


        foreach (var block in cfg.Blocks)
        {
            Console.WriteLine($"Block: {block.Operations.FirstOrDefault()?.Syntax.ToString().Trim() ?? "No syntax available"}");
            IOperation? prevOp = null;
            foreach (var operation in block.Operations)
            {
                Console.WriteLine($"\tOperation: {operation.Syntax.ToString().Trim()}");
                graph.AddNode(operation);

                // Control-Dependencies: current depends on previous
                if (prevOp != null)
                {
                    graph.AddDependency(operation, prevOp); // Corrected order
                    previousInBlock[operation] = prevOp;
                }
                prevOp = operation;

                // Data-Dependencies: track reads and writes
                foreach (var written in GetWrittenSymbols(operation))
                    lastWrite[written] = operation;

                foreach (var read in GetReadSymbols(operation))
                {
                    if (lastWrite.TryGetValue(read, out var writer))
                        graph.AddDependency(operation, writer); // Corrected order
                }
            }
        }

        return graph;
    }

    private IEnumerable<ISymbol> GetWrittenSymbols(IOperation operation)
    {
        // Analizar operaciones que escriben variables
        switch (operation)
        {
            case IAssignmentOperation assign:
                yield return GetSymbol(assign.Target);
                break;
            case IVariableDeclaratorOperation decl:
                yield return decl.Symbol;
                break;
            case IParameterInitializerOperation param:
                yield return param.Parameter;
                break;
        }
    }

    private IEnumerable<ISymbol> GetReadSymbols(IOperation operation)
    {
        // Obtener todas las variables usadas en la operación
        return operation.Descendants()
            .OfType<ILocalReferenceOperation>()
            .Select(r => r.Local)
            .Cast<ISymbol>()
            .Concat(operation.Descendants()
                .OfType<IParameterReferenceOperation>()
                .Select(p => p.Parameter)
                .Cast<ISymbol>());
    }

    private ISymbol GetSymbol(IOperation operation)
    {
        return operation switch
        {
            ILocalReferenceOperation localRef => localRef.Local,
            IParameterReferenceOperation paramRef => paramRef.Parameter,
            IFieldReferenceOperation fieldRef => fieldRef.Field,
            _ => null!
        };
    }
}

public class Program
{
    public static void Main()
    {
        // Uso del código
        var code = @"
public class Example {
    public void Test() {
        int a = 5;
        int b = a + 3;
        if (b > 0) {
            a = b * 2;
        }
        Console.WriteLine(a);
    }
}";
        var syntaxTree = CSharpSyntaxTree.ParseText(code);
        var compilation = CSharpCompilation.Create("Temp")
            .AddReferences(
                MetadataReference.CreateFromFile(typeof(object).Assembly.Location),
                MetadataReference.CreateFromFile(typeof(Console).Assembly.Location))
            .AddSyntaxTrees(syntaxTree);
        var semanticModel = compilation.GetSemanticModel(syntaxTree);

        var method = syntaxTree.GetRoot().DescendantNodes().OfType<MethodDeclarationSyntax>().First();
        var graph = new DependencyGraphBuilder().Build(semanticModel, method);

        // Visualizar dependencias
        foreach (var entry in graph.Dependencies)
        {
            Console.WriteLine($"Operation: {entry.Key.Syntax.ToString().Trim()}");
            foreach (var dep in entry.Value)
            {
                Console.WriteLine($"\t Depends on: {dep.Syntax.ToString().Trim()}");
            }
        }
    }
}

