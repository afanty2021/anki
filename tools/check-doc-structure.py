#!/usr/bin/env python3
"""
文档结构检查工具
验证 CLAUDE.md 文件的结构是否符合标准
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class DocumentStructureChecker:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.issues = []

    def check_all_documents(self) -> bool:
        """检查所有文档"""
        docs = list(self.repo_root.rglob("CLAUDE.md"))

        # 过滤出主要模块的文档
        main_modules = ['ts', 'qt', 'pylib', 'rslib', 'build', 'ftl', 'proto', 'qt/launcher']
        docs = [doc for doc in docs
                if doc.parent == Path('.') or
                str(doc.parent) in main_modules or
                (doc.parent.name == 'qt' and 'launcher' in str(doc.parent))]

        for doc in docs:
            self._check_document(doc)

        return len(self.issues) == 0

    def _check_document(self, doc_path: Path):
        """检查单个文档"""
        relative_path = doc_path.relative_to(self.repo_root)
        module_name = str(relative_path.parent) if relative_path.parent != Path('.') else 'root'

        try:
            content = doc_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception as e:
            self.issues.append(f"{module_name}: 无法读取文件 - {e}")
            return

        # 根文档特殊检查
        if module_name == 'root':
            self._check_root_document(content, lines)
        else:
            self._check_module_document(module_name, content, lines)

        # 通用检查
        self._check_general_structure(module_name, content, lines)

    def _check_root_document(self, content: str, lines: List[str]):
        """检查根文档结构"""
        required_sections = [
            "## 项目愿景",
            "## 架构概览",
            "## 模块结构图",
            "## 模块索引",
            "## 运行和开发",
            "## 更新日志"
        ]

        for section in required_sections:
            if section not in content:
                self.issues.append(f"根文档缺少必要章节: {section}")

        # 检查 Mermaid 图表
        if "```mermaid" not in content:
            self.issues.append("根文档缺少 Mermaid 模块结构图")

        # 检查模块索引表
        if "模块路径" not in content or "语言/技术栈" not in content:
            self.issues.append("根文档缺少模块索引表")

    def _check_module_document(self, module_name: str, content: str, lines: List[str]):
        """检查模块文档结构"""
        # 检查必要章节
        required_sections = ["#", "##"]

        has_title = any(line.startswith('# ') for line in lines)
        if not has_title:
            self.issues.append(f"{module_name}: 缺少文档标题")

        has_sections = any(line.startswith('## ') for line in lines)
        if not has_sections:
            self.issues.append(f"{module_name}: 缺少章节标题")

        # 检查导航面包屑
        if "> 项目集合" not in content and module_name != 'root':
            self.issues.append(f"{module_name}: 缺少导航面包屑")

    def _check_general_structure(self, module_name: str, content: str, lines: List[str]):
        """通用结构检查"""
        # 检查空行过多
        consecutive_empty = 0
        max_consecutive = 3

        for line in lines:
            if line.strip() == '':
                consecutive_empty += 1
                if consecutive_empty > max_consecutive:
                    self.issues.append(f"{module_name}: 发现过多连续空行 (>{max_consecutive})")
                    break
            else:
                consecutive_empty = 0

        # 检查标题层级
        prev_level = 0
        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                if level > prev_level + 1:
                    self.issues.append(f"{module_name}: 标题层级跳跃过大 (从 h{prev_level} 到 h{level})")
                prev_level = level

        # 检查中文标点
        chinese_punctuation_issues = re.findall(r'[a-zA-Z0-9][，。！？；：]', content)
        if chinese_punctuation_issues:
            self.issues.append(f"{module_name}: 发现中英文混用标点 (如 '{chinese_punctuation_issues[0]}')")

    def generate_report(self) -> str:
        """生成检查报告"""
        if not self.issues:
            return "✅ 所有文档结构检查通过"

        report = ["❌ 发现以下文档结构问题：\n"]
        for i, issue in enumerate(self.issues, 1):
            report.append(f"{i}. {issue}")

        return "\n".join(report)

def main():
    repo_root = Path.cwd()
    if not (repo_root / ".git").exists():
        print("❌ 错误: 不在 Git 仓库中")
        sys.exit(1)

    checker = DocumentStructureChecker(repo_root)

    if checker.check_all_documents():
        print(checker.generate_report())
        sys.exit(0)
    else:
        print(checker.generate_report())
        sys.exit(1)

if __name__ == "__main__":
    main()