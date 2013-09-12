(TeX-add-style-hook "DataMining"
 (lambda ()
    (LaTeX-add-environments
     "theorem"
     "problem"
     "definition"
     "lemma")
    (TeX-add-symbols
     '("norm" 1)
     '("Voronoi" 1)
     '("massCenter" 1)
     '("dotProd" 2)
     '("SV" 2)
     '("sv" 2)
     '("transpose" 1)
     '("mat" 1)
     "RR"
     "Set"
     "bSet"
     "cR")
    (TeX-run-style-hooks
     "amsthm"
     "amssymb"
     "babel"
     "english"
     "amsmath")))

