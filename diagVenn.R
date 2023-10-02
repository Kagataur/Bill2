# install.packages("VennDiagram")
library("VennDiagram")
## mapping avec Sniffle :
draw.triple.venn(area1 = 6, # P15
                 area2 = 5, # P50
                 area3 = 2, # P30
                 n12  = 1,
                 n23  = 1,
                 n13  = 1,
                 n123 = 1,
                 fill = c('pink','green','orange'),
                 lty = 'blank',
                 category = c('P15','P50','P30'))
# n12 : P15P30 ; n23 : P30P50 ; n13 : P15P50

## mapping avec :
draw.triple.venn(area1 = 8 ,  # nanovar
                 area2 = 6,   # sniffle
                 area3 = 694, # swim
                 n12  = 0,
                 n23  = 1,
                 n13  = 0,
                 n123 = 0,
                 fill = c('pink','green','orange'),
                 lty = 'blank',
                 category = c('nanovar','sniffle','swim'))


# nanovar :  8
# sniffle : 6
# swim : 694