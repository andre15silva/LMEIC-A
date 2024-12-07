#ifndef __OG_POINTER_INDEX_NODE_H__
#define __OG_POINTER_INDEX_NODE_H__

#include <cdk/ast/expression_node.h>
#include <cdk/ast/lvalue_node.h>

namespace og {
/*
  Class for describing pointer index nodes.
 */

class pointer_index_node : public cdk::lvalue_node {
private:
    cdk::expression_node *_base;
    cdk::expression_node *_index;

public:
    pointer_index_node(int lineno, cdk::expression_node *base,
                       cdk::expression_node *index)
        : cdk::lvalue_node(lineno), _base(base), _index(index) {}

    cdk::expression_node *base() { return _base; }
    cdk::expression_node *index() { return _index; }

    void accept(basic_ast_visitor *sp, int level) {
        sp->do_pointer_index_node(this, level);
    }
};
} // namespace og

#endif
