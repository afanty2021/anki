#!/bin/bash
# 文档质量检查脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 统计变量
ERRORS=0
WARNINGS=0

# 错误计数函数
error() {
    echo -e "${RED}❌ $1${NC}"
    ((ERRORS++))
}

# 警告计数函数
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

# 成功信息函数
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 信息函数
info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 检查必要的工具
check_tools() {
    info "检查必要的工具..."

    # 检查 markdownlint
    if ! command -v markdownlint &> /dev/null; then
        warning "markdownlint 未安装，跳过 Markdown 语法检查"
        echo "  安装方法: npm install -g markdownlint-cli"
    fi

    # 检查 markdown-link-check
    if ! command -v markdown-link-check &> /dev/null; then
        warning "markdown-link-check 未安装，跳过链接检查"
        echo "  安装方法: npm install -g markdown-link-check"
    fi

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 未安装"
        return 1
    fi
}

# 查找所有 CLAUDE.md 文件
find_doc_files() {
    find "$REPO_ROOT" -name "CLAUDE.md" -type f | sort
}

# Markdown 语法检查
check_markdown_syntax() {
    info "检查 Markdown 语法..."

    local doc_files=($(find_doc_files))
    local syntax_errors=0

    if command -v markdownlint &> /dev/null && [ ${#doc_files[@]} -gt 0 ]; then
        # 创建临时配置文件
        local config_file=$(mktemp)
        cat > "$config_file" <<'EOF'
{
  "default": true,
  "MD013": false,  # 行长度限制（禁用，因为中文需要）
  "MD033": false,  # HTML 标签（允许，因为需要特殊格式）
  "MD041": false,  # 第一行必须是标题（允许灵活性）
  "MD007": { "indent": 2 },  # 列表缩进
  "MD029": { "style": "ordered" }  # 有序列表样式
}
EOF

        for doc_file in "${doc_files[@]}"; do
            if ! markdownlint --config "$config_file" "$doc_file"; then
                ((syntax_errors++))
            fi
        done

        rm -f "$config_file"

        if [ $syntax_errors -eq 0 ]; then
            success "所有 Markdown 文件语法正确"
        else
            error "发现 $syntax_errors 个 Markdown 语法错误"
        fi
    fi
}

# 检查链接有效性
check_links() {
    info "检查链接有效性..."

    local doc_files=($(find_doc_files))
    local link_errors=0

    if command -v markdown-link-check &> /dev/null && [ ${#doc_files[@]} -gt 0 ]; then
        # 创建临时配置文件
        local config_file=$(mktemp)
        cat > "$config_file" <<'EOF'
{
  "ignorePatterns": [
    {
      "pattern": "^http://localhost"
    },
    {
      "pattern": "^#"
    }
  ],
  "replacementPatterns": [],
  "httpHeaders": [],
  "timeout": "20s",
  "retryOn429": true,
  "retryCount": 3,
  "fallbackRetryDelay": "30s"
}
EOF

        for doc_file in "${doc_files[@]}"; do
            echo "  检查链接: $(basename $(dirname "$doc_file"))/CLAUDE.md"
            if ! markdown-link-check --config "$config_file" "$doc_file" --verbose; then
                ((link_errors++))
            fi
        done

        rm -f "$config_file"

        if [ $link_errors -eq 0 ]; then
            success "所有链接有效"
        else
            error "发现 $link_errors 个无效链接"
        fi
    fi
}

# 检查文档结构
check_document_structure() {
    info "检查文档结构..."

    python3 "$SCRIPT_DIR/check-doc-structure.py" 2>/dev/null || {
        warning "文档结构检查脚本不存在，执行基本检查..."

        # 基本结构检查
        local doc_files=($(find_doc_files))
        local structure_errors=0

        for doc_file in "${doc_files[@]}"; do
            local dir_name=$(basename "$(dirname "$doc_file")")

            # 检查必要章节
            local required_sections=()
            if [ "$dir_name" = "anki" ]; then
                required_sections=("## 项目愿景" "## 架构概览" "## 模块结构图" "## 模块索引")
            else
                required_sections=("#" "##" "###")
            fi

            for section in "${required_sections[@]}"; do
                if ! grep -q "$section" "$doc_file"; then
                    warning "$dir_name/CLAUDE.md 缺少章节: $section"
                    ((structure_errors++))
                fi
            done
        done

        if [ $structure_errors -eq 0 ]; then
            success "文档结构检查通过"
        else
            warning "发现 $structure_errors 个结构问题"
        fi
    }
}

# 检查 Mermaid 图表
check_mermaid_diagrams() {
    info "检查 Mermaid 图表..."

    local doc_files=($(find_doc_files))
    local mermaid_errors=0

    for doc_file in "${doc_files[@]}"; do
        # 提取所有 Mermaid 代码块
        local mermaid_blocks=$(sed -n '/```mermaid/,/```/p' "$doc_file" | grep -v '```')

        if [ -n "$mermaid_blocks" ]; then
            # 基本语法检查
            if echo "$mermaid_blocks" | grep -q "graph TD\|graph LR\|flowchart TD\|flowchart LR"; then
                # 检查是否有节点定义
                local node_count=$(echo "$mermaid_blocks" | grep -o '\[.*\]' | wc -l)
                local arrow_count=$(echo "$mermaid_blocks" | grep -o '-->\|-->|==>|-.->' | wc -l)

                if [ $node_count -eq 0 ] && [ $arrow_count -eq 0 ]; then
                    warning "$(basename $(dirname "$doc_file")): Mermaid 图表可能不完整"
                    ((mermaid_errors++))
                fi
            fi
        fi
    done

    if [ $mermaid_errors -eq 0 ]; then
        success "Mermaid 图表检查通过"
    else
        warning "发现 $mermaid_errors 个 Mermaid 图表问题"
    fi
}

# 检查导航链接
check_navigation_links() {
    info "检查导航链接..."

    local root_doc="$REPO_ROOT/CLAUDE.md"
    if [ -f "$root_doc" ]; then
        # 检查模块链接
        local missing_links=0
        local modules=("ts" "qt" "pylib" "rslib" "build" "ftl" "proto")

        for module in "${modules[@]}"; do
            if ! grep -q "./$module/CLAUDE.md" "$root_doc"; then
                warning "根文档缺少模块 $module 的链接"
                ((missing_links++))
            fi
        done

        # 检查链接有效性
        for module in "${modules[@]}"; do
            local module_doc="$REPO_ROOT/$module/CLAUDE.md"
            if grep -q "./$module/CLAUDE.md" "$root_doc" && [ ! -f "$module_doc" ]; then
                error "链接指向不存在的文件: ./$module/CLAUDE.md"
                ((missing_links++))
            fi
        done

        if [ $missing_links -eq 0 ]; then
            success "导航链接检查通过"
        else
            error "发现 $missing_links 个导航链接问题"
        fi
    fi
}

# 检查一致性
check_consistency() {
    info "检查文档一致性..."

    python3 "$SCRIPT_DIR/check-doc-consistency.py" 2>/dev/null || {
        warning "一致性检查脚本不存在，跳过"
    }
}

# 生成检查报告
generate_report() {
    echo -e "\n${BLUE}📊 文档质量检查报告${NC}"
    echo "====================================="
    echo "错误数: $ERRORS"
    echo "警告数: $WARNINGS"
    echo ""

    if [ $ERRORS -eq 0 ]; then
        if [ $WARNINGS -eq 0 ]; then
            success "文档质量检查全部通过！"
            return 0
        else
            warning "文档质量检查通过，但有 $WARNINGS 个警告"
            return 1
        fi
    else
        error "文档质量检查失败，有 $ERRORS 个错误需要修复"
        return 1
    fi
}

# 主函数
main() {
    echo -e "${GREEN}🔍 开始文档质量检查...${NC}\n"

    check_tools
    check_markdown_syntax
    check_links
    check_document_structure
    check_mermaid_diagrams
    check_navigation_links
    check_consistency

    echo ""
    generate_report
}

# 处理命令行参数
case "${1:-}" in
    --help|-h)
        echo "文档质量检查脚本"
        echo ""
        echo "用法: $0 [选项]"
        echo ""
        echo "选项:"
        echo "  --help, -h     显示此帮助信息"
        echo "  --syntax-only  仅检查语法"
        echo "  --links-only   仅检查链接"
        echo ""
        exit 0
        ;;
    --syntax-only)
        check_tools
        check_markdown_syntax
        generate_report
        exit $?
        ;;
    --links-only)
        check_tools
        check_links
        generate_report
        exit $?
        ;;
esac

main