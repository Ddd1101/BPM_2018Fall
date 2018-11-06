```
Date:2018-11-06
```

### Description

The states of the system (**places**) include:

* P1: author
* P2: articles to be reviewed
* P3: chief editor
* P4: editor
* P5: articles to be final reviewed
* P6: passed articles

Events (**transitions**) include:

* T1: submit an article
* T2: show to chief editor
* T3: assign editors
* T4: review articles
* T5: refuse articles
* T6: pass articles
* T7: check articles
* T8: modify articles
* T9: withdraw articles

Five tokens are needed for completing the business process:

* the author submits an article which will be accepted
  * P1 → P2 → P3 → P4 → P5 → P3 → P6
  * Events: T1, T2, T3, T4, T2, T6
* the author submits an article which will be refused
  * P1 → P2 → P3 → P4 → P5 → P3 → P2
  * Events: T1, T2, T3, T4, T2, T5
* the author checks a submitted article and modifies it
  * P1 → P2 
  * Events: T7, T8
* the author checks a reviewed article and modifies it
  * P1 → P5
  * Events: T7, T8
* withdraw an article
  * P6 → P1
  * Events: T9

It's obvious that the articles is the main value of the system. It must ensure the articles' quality and amount.   The more articles to be published, the more users to be drawn; the better articles to be published, the more authors to be drawn. This forms a  virtuous circle and that's why the main path, which contains all actors in the system, is **REVIEW**. Efficiency of editors and the chief editor coping with articles is the bottleneck, hence KPI depends on the chief editor and editors. To manage articles better, system should have good policies to store articles and tag them accurately.