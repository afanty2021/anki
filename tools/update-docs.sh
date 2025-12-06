#!/bin/bash
# Anki 文档自动更新脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}🔍 检查依赖...${NC}"

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 未安装${NC}"
        exit 1
    fi

    # 检查 Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git 未安装${NC}"
        exit 1
    fi

    echo -e "${GREEN}✅ 依赖检查通过${NC}"
}

# 检查工作目录状态
check_working_directory() {
    echo -e "${BLUE}📋 检查工作目录状态...${NC}"

    if [[ -n $(git status --porcelain) ]]; then
        echo -e "${YELLOW}⚠️  工作目录有未提交的变更${NC}"
        echo -e "${YELLOW}   建议先提交或暂存变更${NC}"

        read -p "是否继续？(y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
}

# 检测需要更新的文档
detect_updates() {
    echo -e "${BLUE}🔍 检测需要更新的文档...${NC}"

    if python3 "$SCRIPT_DIR/sync-docs.py" --check-only > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 文档已是最新，无需更新${NC}"
        exit 0
    fi

    # 生成更新计划
    python3 "$SCRIPT_DIR/sync-docs.py" --output "$REPO_ROOT/.doc-update-plan.md"
    echo -e "${GREEN}📝 更新计划已生成${NC}"
}

# 备份当前文档
backup_docs() {
    echo -e "${BLUE}💾 备份当前文档...${NC}"

    BACKUP_DIR="$REPO_ROOT/.doc-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # 备份所有 CLAUDE.md 文件
    find "$REPO_ROOT" -name "CLAUDE.md" -not -path "$BACKUP_DIR/*" -exec cp --parents {} "$BACKUP_DIR" \;

    echo -e "${GREEN}✅ 文档已备份到 $BACKUP_DIR${NC}"
}

# 生成模块文档更新
generate_module_updates() {
    echo -e "${BLUE}🔄 生成模块文档更新...${NC}"

    # 如果存在模块文档生成脚本，运行它
    if [[ -f "$SCRIPT_DIR/generate-module-docs.py" ]]; then
        python3 "$SCRIPT_DIR/generate-module-docs.py"
    else
        echo -e "${YELLOW}⚠️  模块文档生成脚本不存在，跳过${NC}"
    fi
}

# 更新根文档
update_root_doc() {
    echo -e "${BLUE}📊 更新根文档统计信息...${NC}"

    # 如果存在根文档更新脚本，运行它
    if [[ -f "$SCRIPT_DIR/update-root-doc.py" ]]; then
        python3 "$SCRIPT_DIR/update-root-doc.py"
    else
        echo -e "${YELLOW}⚠️  根文档更新脚本不存在，手动更新统计信息${NC}"

        # 更新根文档中的文件统计
        python3 -c "
import json
from pathlib import Path
from datetime import datetime

# 读取根文档
root_doc = Path('$REPO_ROOT/CLAUDE.md')
if not root_doc.exists():
    exit(0)

content = root_doc.read_text(encoding='utf-8')

# 更新文档更新日志
today = datetime.now().strftime('%Y-%m-%d')
log_entry = f'- {today}: 自动同步更新，根据代码变更更新模块文档和统计信息'

# 查找更新日志部分
lines = content.split('\n')
new_lines = []
inserted = False

for i, line in enumerate(lines):
    new_lines.append(line)
    if line.startswith('## 更新日志') and not inserted:
        new_lines.append(log_entry)
        inserted = True
        break

# 如果没找到更新日志部分，在项目愿景后添加
if not inserted:
    for i, line in enumerate(lines):
        if line.startswith('## 项目愿景'):
            new_lines.append('')
            new_lines.append('## 更新日志')
            new_lines.append(log_entry)
            inserted = True
            break

# 写回文件
root_doc.write_text('\n'.join(new_lines + lines[i+1:]), encoding='utf-8')
print('✅ 根文档更新完成')
"
    fi
}

# 验证文档质量
validate_docs() {
    echo -e "${BLUE}✅ 验证文档质量...${NC}"

    # 如果存在文档检查脚本，运行它
    if [[ -f "$SCRIPT_DIR/check-docs.sh" ]]; then
        "$SCRIPT_DIR/check-docs.sh"
    else
        echo -e "${YELLOW}⚠️  文档检查脚本不存在，跳过质量验证${NC}"
    fi
}

# 记录更新时间
record_update_time() {
    echo -e "${BLUE}📝 记录更新时间...${NC}"
    echo "$(date -u +%Y-%m-%dT%H:%M:%S)" > "$REPO_ROOT/.last-doc-sync"
    echo -e "${GREEN}✅ 更新时间已记录${NC}"
}

# 显示更新摘要
show_summary() {
    echo -e "\n${GREEN}✨ 文档更新完成！${NC}\n"

    echo -e "${YELLOW}💡 建议的后续操作：${NC}"
    echo "1. 查看更新计划: cat .doc-update-plan.md"
    echo "2. 检查变更: git diff --name-only | grep CLAUDE.md"
    echo "3. 提交变更:"
    echo "   git add ."
    echo "   git commit -m \"docs: 更新上下文文档 ($(date +%Y-%m-%d))\""
    echo "   git push origin main"
    echo ""

    if [[ -f "$REPO_ROOT/.doc-update-plan.md" ]]; then
        echo -e "${BLUE}📋 更新计划摘要：${NC}"
        head -20 "$REPO_ROOT/.doc-update-plan.md"
        echo "..."
    fi
}

# 主函数
main() {
    echo -e "${GREEN}🚀 开始更新 Anki 上下文文档...${NC}\n"

    check_dependencies
    check_working_directory
    detect_updates
    backup_docs
    generate_module_updates
    update_root_doc
    validate_docs
    record_update_time
    show_summary
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "Anki 文档自动更新脚本"
        echo ""
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  --help, -h     显示此帮助信息"
        echo "  --check-only   仅检查是否需要更新"
        echo "  --no-backup    跳过文档备份"
        echo ""
        exit 0
        ;;
    --check-only)
        python3 "$SCRIPT_DIR/sync-docs.py"
        exit $?
        ;;
    --no-backup)
        echo -e "${YELLOW}⚠️  跳过文档备份${NC}"
        CHECK_ONLY=true
        ;;
esac

main