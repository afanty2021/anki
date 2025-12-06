#!/usr/bin/env python3
"""
Anki 文档同步检测工具
检测代码变更并识别需要更新的文档
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional
import argparse

class DocSyncDetector:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.doc_files = self._find_doc_files()
        self.last_sync = self._get_last_sync_time()

    def _find_doc_files(self) -> Dict[str, Path]:
        """查找所有 CLAUDE.md 文件"""
        docs = {}
        for doc_file in self.repo_root.rglob("CLAUDE.md"):
            rel_path = doc_file.relative_to(self.repo_root)
            # 只记录主要模块的文档，忽略其他目录
            if rel_path.parent in [Path(p) for p in ['ts', 'qt', 'pylib', 'rslib', 'build', 'ftl', 'proto', 'qt/launcher']]:
                docs[str(rel_path.parent)] = doc_file
            elif rel_path.parent == Path('.'):
                docs['root'] = doc_file
        return docs

    def _get_last_sync_time(self) -> datetime:
        """获取上次文档同步时间"""
        sync_file = self.repo_root / ".last-doc-sync"
        try:
            with open(sync_file, "r") as f:
                timestamp = f.read().strip()
                return datetime.fromisoformat(timestamp)
        except FileNotFoundError:
            # 默认返回一周前
            return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)

    def detect_changes(self, since: Optional[datetime] = None) -> Dict[str, List[str]]:
        """检测需要更新的文档"""
        if since is None:
            since = self.last_sync

        # 获取自指定时间以来的变更
        git_cmd = ["git", "log", f"--since={since.isoformat()}", "--name-only", "--pretty=format:"]
        result = subprocess.run(git_cmd, capture_output=True, text=True, cwd=self.repo_root)

        changes = [line for line in result.stdout.splitlines() if line.strip()]

        affected_modules = self._analyze_changes(changes)
        return affected_modules

    def _analyze_changes(self, changes: List[str]) -> Dict[str, List[str]]:
        """分析变更影响的模块"""
        affected = {
            "root": [],  # 根文档
            "modules": {},  # 模块文档
            "new_files": [],
            "deleted_files": [],
            "moved_files": []
        }

        for change in changes:
            if not change or change.startswith('#'):
                continue

            # 确定变更的模块
            module = self._get_module_for_file(change)

            # 分类变更类型
            if Path(change).suffix in ['.rs', '.py', '.ts', '.js', '.svelte', '.proto', 'md']:
                if module and module in self.doc_files:
                    if module not in affected["modules"]:
                        affected["modules"][module] = []
                    affected["modules"][module].append(change)

                # 某些变更总是影响根文档
                if self._affects_root_doc(change):
                    affected["root"].append(change)

        # 检测新增和删除的模块
        self._detect_module_changes(affected)

        return affected

    def _get_module_for_file(self, file_path: str) -> Optional[str]:
        """获取文件所属的模块"""
        path_parts = Path(file_path).parts
        if len(path_parts) >= 1:
            module = path_parts[0]
            if module == 'qt' and len(path_parts) >= 2 and path_parts[1] == 'launcher':
                return 'qt/launcher'
            return module
        return None

    def _affects_root_doc(self, file_path: str) -> bool:
        """判断变更是否影响根文档"""
        indicators = [
            "CLAUDE.md",      # 文档本身
            "proto/",         # 接口变更
            "build/",         # 构建系统变更
            "Cargo.toml",     # Rust 依赖变更
            "package.json",   # Node.js 依赖变更
            "pyproject.toml", # Python 项目配置
            "requirements.txt", # Python 依赖
            "ninja",          # 构建相关
            "workspace",      # Rust workspace
        ]
        return any(indicator in file_path for indicator in indicators)

    def _detect_module_changes(self, affected: Dict):
        """检测新增或删除的模块"""
        existing_modules = set(self.doc_files.keys())
        changed_modules = set()

        # 从变更中提取模块
        for change in affected["modules"]:
            changed_modules.add(change)
        for change in affected["root"]:
            module = self._get_module_for_file(change)
            if module:
                changed_modules.add(module)

        # 这里简化处理，实际可以更精确地检测新增/删除
        pass

    def generate_update_plan(self, changes: Dict) -> str:
        """生成更新计划"""
        plan = []
        plan.append("# 文档更新计划\n")
        plan.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        if changes["root"]:
            plan.append("## 需要更新根文档 (CLAUDE.md)")
            plan.append(f"- 原因: {len(changes['root'])} 个文件变更")
            plan.append("- 更新内容:")
            for change in changes["root"][:5]:  # 只显示前5个
                plan.append(f"  - {change}")
            if len(changes["root"]) > 5:
                plan.append(f"  - ... 还有 {len(changes['root']) - 5} 个文件")
            plan.append("")

        if changes["modules"]:
            plan.append("## 需要更新的模块文档")
            for module, files in changes["modules"].items():
                plan.append(f"### {module}/CLAUDE.md")
                plan.append(f"- 变更文件数: {len(files)}")
                if files:
                    plan.append("- 主要变更:")
                    for file in files[:3]:  # 只显示前3个
                        plan.append(f"  - {file}")
                    if len(files) > 3:
                        plan.append(f"  - ... 还有 {len(files) - 3} 个文件")
                plan.append("")

        if not changes["root"] and not changes["modules"]:
            plan.append("✅ 检测结果: 无需更新文档")

        plan.append("## 建议的操作")
        plan.append("1. 运行 `./tools/update-docs.sh` 自动更新")
        plan.append("2. 或手动执行以下命令:")
        plan.append("   - 更新根文档: `python3 tools/update-root-doc.py`")
        plan.append("   - 更新模块文档: `python3 tools/generate-module-docs.py`")
        plan.append("3. 验证更新: `./tools/check-docs.sh`")

        return "\n".join(plan)

    def check_only(self) -> int:
        """仅检查是否需要更新，返回退出码"""
        changes = self.detect_changes()

        if changes["root"] or changes["modules"]:
            print("⚠️  检测到需要更新的文档")
            return 1
        else:
            print("✅ 文档已是最新")
            return 0

def main():
    parser = argparse.ArgumentParser(description="Anki 文档同步检测工具")
    parser.add_argument("--check-only", action="store_true", help="仅检查是否需要更新")
    parser.add_argument("--since", help="指定起始日期 (YYYY-MM-DD)")
    parser.add_argument("--output", help="输出更新计划到文件")
    parser.add_argument("--ci-mode", action="store_true", help="CI 模式，输出 JSON 格式")

    args = parser.parse_args()

    repo_root = Path.cwd()
    if not (repo_root / ".git").exists():
        print("❌ 错误: 不在 Git 仓库中")
        sys.exit(1)

    detector = DocSyncDetector(repo_root)

    # 解析起始时间
    since = None
    if args.since:
        try:
            since = datetime.fromisoformat(args.since)
        except ValueError:
            print(f"❌ 错误: 无效的日期格式 {args.since}")
            sys.exit(1)

    changes = detector.detect_changes(since)

    if args.check_only:
        sys.exit(detector.check_only())

    if args.ci_mode:
        # CI 模式输出 JSON
        ci_output = {
            "needs_update": bool(changes["root"] or changes["modules"]),
            "changes": changes,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(ci_output, indent=2))
    else:
        # 生成更新计划
        plan = detector.generate_update_plan(changes)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(plan)
            print(f"✅ 更新计划已保存到 {args.output}")
        else:
            print(plan)

if __name__ == "__main__":
    main()