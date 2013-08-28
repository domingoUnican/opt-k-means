(TeX-add-style-hook "KDD"
 (lambda ()
    (LaTeX-add-bibliographies
     "bibliography")
    (LaTeX-add-labels
     "sec:BasicConceptsClustering"
     "lem:maximum_separation"
     "sec:reverse_enumeration"
     "prob:traversal"
     "alg:reverse_enumeration"
     "sec:two_clusters"
     "sec:sub_local_search"
     "alg:naive"
     "alg:sleumer")
    (TeX-add-symbols
     "cH")
    (TeX-run-style-hooks
     "algorithmic"
     "algorithm"
     "latex2e"
     "art10"
     "article"
     "DataMining")))

