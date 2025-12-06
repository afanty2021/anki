#!/usr/bin/env python3
"""
Mermaid 图表语法检查工具
验证 Mermaid 图表的基本语法正确性
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class MermaidSyntaxChecker:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def check_all_documents(self, repo_root: Path) -> bool:
        """检查所有文档中的 Mermaid 图表"""
        doc_files = list(repo_root.rglob("CLAUDE.md"))

        # 过滤出主要模块的文档
        main_modules = ['ts', 'qt', 'pylib', 'rslib', 'build', 'ftl', 'proto', 'qt/launcher']
        doc_files = [doc for doc in doc_files
                    if doc.parent == Path('.') or
                    str(doc.parent) in main_modules or
                    (doc.parent.name == 'qt' and 'launcher' in str(doc.parent))]

        for doc_file in doc_files:
            self._check_document(doc_file)

        return len(self.errors) == 0

    def _check_document(self, doc_path: Path):
        """检查单个文档中的 Mermaid 图表"""
        try:
            content = doc_path.read_text(encoding='utf-8')
            module_name = str(doc_path.relative_to(doc_path.parents[1]).parent)

            # 提取所有 Mermaid 代码块
            mermaid_blocks = self._extract_mermaid_blocks(content)

            for i, block in enumerate(mermaid_blocks, 1):
                self._check_mermaid_block(module_name, i, block)

        except Exception as e:
            self.errors.append(f"无法读取 {doc_path}: {e}")

    def _extract_mermaid_blocks(self, content: str) -> List[str]:
        """提取所有 Mermaid 代码块"""
        blocks = []
        in_mermaid = False
        current_block = []

        for line in content.split('\n'):
            if line.strip() == '```mermaid':
                in_mermaid = True
                current_block = []
            elif line.strip() == '```' and in_mermaid:
                in_mermaid = False
                if current_block:
                    blocks.append('\n'.join(current_block))
            elif in_mermaid:
                current_block.append(line)

        return blocks

    def _check_mermaid_block(self, module_name: str, block_num: int, block: str):
        """检查单个 Mermaid 块"""
        lines = [line.strip() for line in block.split('\n') if line.strip()]

        if not lines:
            self.warnings.append(f"{module_name}: 第 {block_num} 个 Mermaid 图表为空")
            return

        # 检查图表类型
        chart_type = self._detect_chart_type(lines[0])
        if not chart_type:
            self.errors.append(f"{module_name}: 第 {block_num} 个 Mermaid 图表无法识别类型")
            return

        # 根据图表类型进行特定检查
        if chart_type in ['graph', 'flowchart']:
            self._check_graph_chart(module_name, block_num, lines)
        elif chart_type == 'sequenceDiagram':
            self._check_sequence_diagram(module_name, block_num, lines)
        elif chart_type == 'classDiagram':
            self._check_class_diagram(module_name, block_num, lines)

    def _detect_chart_type(self, first_line: str) -> str:
        """检测图表类型"""
        types = {
            'graph': ['graph TD', 'graph LR', 'graph TB', 'graph BT', 'graph RL'],
            'flowchart': ['flowchart TD', 'flowchart LR', 'flowchart TB', 'flowchart BT', 'flowchart RL'],
            'sequenceDiagram': ['sequenceDiagram'],
            'classDiagram': ['classDiagram'],
            'pie': ['pie'],
            'gantt': ['gantt'],
        }

        for chart_type, patterns in types.items():
            if any(first_line.startswith(pattern) for pattern in patterns):
                return chart_type

        return None

    def _check_graph_chart(self, module_name: str, block_num: int, lines: List[str]):
        """检查流程图语法"""
        nodes = set()
        edges = []

        for line in lines[1:]:  # 跳过第一行（图表类型声明）
            # 匹配节点定义
            node_match = re.match(r'(\w+)(\["[^"]+"\]|\["[^"]+"\]|\([^)]+\)|\[[^\]]+\]|\{[^}]+\})?', line)
            if node_match:
                nodes.add(node_match.group(1))

            # 匹配边定义
            edge_match = re.search(r'(\w+)\s*(-->|--->|==>|===|-.->|->)\s*(\w+)', line)
            if edge_match:
                edges.append((edge_match.group(1), edge_match.group(3)))

        # 检查是否有足够的节点
        if len(nodes) < 2:
            self.warnings.append(f"{module_name}: 第 {block_num} 个流程图节点较少 ({len(nodes)} 个)")

        # 检查边引用的节点是否存在
        for src, dst in edges:
            if src not in nodes:
                self.errors.append(f"{module_name}: 第 {block_num} 个流程图引用了不存在的源节点 '{src}'")
            if dst not in nodes:
                self.errors.append(f"{module_name}: 第 {block_num} 个流程图引用了不存在的目标节点 '{dst}'")

        # 检查子图语法
        subgraph_count = sum(1 for line in lines if line.startswith('subgraph'))
        end_count = sum(1 for line in lines if line == 'end')

        if subgraph_count != end_count:
            self.errors.append(f"{module_name}: 第 {block_num} 个流程图的 subgraph/end 不匹配")

    def _check_sequence_diagram(self, module_name: str, block_num: int, lines: List[str]):
        """检查时序图语法"""
        participants = []
        messages = []

        for line in lines[1:]:
            # 匹配参与者定义
            participant_match = re.match(r'participant\s+(\w+)', line)
            if participant_match:
                participants.append(participant_match.group(1))

            # 匹配消息
            message_match = re.match(r'(\w+)\s*->>\s*(\w+)\s*:\s*(.+)', line)
            if message_match:
                messages.append((message_match.group(1), message_match.group(2)))

        # 检查消息引用的参与者
        for src, dst in messages:
            if src not in participants and not any(p.startswith(src) for p in participants):
                self.warnings.append(f"{module_name}: 第 {block_num} 个时序图消息源 '{src}' 未在参与者中定义")
            if dst not in participants and not any(p.startswith(dst) for p in participants):
                self.warnings.append(f"{module_name}: 第 {block_num} 个时序图消息目标 '{dst}' 未在参与者中定义")

    def _check_class_diagram(self, module_name: str, block_num: int, lines: List[str]):
        """检查类图语法"""
        classes = []
        relationships = []

        for line in lines[1:]:
            # 匹配类定义
            class_match = re.match(r'class\s+(\w+)', line)
            if class_match:
                classes.append(class_match.group(1))

            # 匹配关系
            rel_match = re.match(r'(\w+)\s*(-->|<--|--|\*--|o--)\s*(\w+)', line)
            if rel_match:
                relationships.append((rel_match.group(1), rel_match.group(3)))

        # 检查关系引用的类是否存在
        for src, dst in relationships:
            if src not in classes:
                self.warnings.append(f"{module_name}: 第 {block_num} 个类图关系源类 '{src}' 未定义")
            if dst not in classes:
                self.warnings.append(f"{module_name}: 第 {block_num} 个类图关系目标类 '{dst}' 未定义")

    def generate_report(self) -> str:
        """生成检查报告"""
        if not self.errors and not self.warnings:
            return "✅ 所有 Mermaid 图表语法检查通过"

        report_lines = []

        if self.errors:
            report_lines.append("❌ 发现以下 Mermaid 语法错误：\n")
            for i, error in enumerate(self.errors, 1):
                report_lines.append(f"{i}. {error}")

        if self.warnings:
            if self.errors:
                report_lines.append("\n")
            report_lines.append("⚠️  发现以下 Mermaid 语法警告：\n")
            for i, warning in enumerate(self.warnings, 1):
                report_lines.append(f"{i}. {warning}")

        return "\n".join(report_lines)

def main():
    if len(sys.argv) > 1:
        repo_root = Path(sys.argv[1])
    else:
        repo_root = Path.cwd()

    if not (repo_root / ".git").exists():
        print("❌ 错误: 不在 Git 仓库中")
        sys.exit(1)

    checker = MermaidSyntaxChecker()

    if checker.check_all_documents(repo_root):
        print(checker.generate_report())
        sys.exit(0)
    else:
        print(checker.generate_report())
        sys.exit(1)

if __name__ == "__main__":
    main()