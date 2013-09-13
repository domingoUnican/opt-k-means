(TeX-add-style-hook "KDD"
 (lambda ()
    (LaTeX-add-bibliographies
     "bibliography")
    (LaTeX-add-labels
     "sec:BasicConceptsClustering"
     "lem:maximum_separation"
     "lem:properties_clusters"
     "sec:reverse_enumeration"
     "prob:traversal"
     "alg:reverse_enumeration"
     "thm:complexity"
     "sec:two_clusters"
     "sec:sub_local_search"
     "alg:naive"
     "alg:sleumer"
     "eq:definition_H_R"
     "lem:k-1-hyperplanes")
    (TeX-add-symbols
     "cH")
    (TeX-run-style-hooks
     "algorithmic"
     "algorithm"
     "latex2e"
     "art10"
     "article"
     "DataMining")))

