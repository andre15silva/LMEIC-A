#ifndef __OG_AST_STACK_ALLOC_H__
#define __OG_AST_STACK_ALLOC_H__

#include "targets/basic_ast_visitor.h"
#include <cdk/ast/unary_operation_node.h>
#include <cdk/ast/expression_node.h>

namespace og {

class stack_alloc_node : public cdk::unary_operation_node {
public:
    stack_alloc_node(int lineno, cdk::expression_node *argument)
        : cdk::unary_operation_node(lineno, argument) {}

    void accept(basic_ast_visitor *sp, int level) {
        sp->do_stack_alloc_node(this, level);
    }
};

} // namespace og

#endif