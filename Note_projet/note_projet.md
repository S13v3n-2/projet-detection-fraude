Beaucoup de point sur EDA (traitement de la données).

Il faut un modéle de machine superviser et un modéle de machine non-superviser

On a un échantillonnage de données très déséquilibrées
![img.png](img.png)

on va utilise

2. Le F1-ScoreLe F1-Score est la moyenne "intelligente" (harmonique) entre deux concepts clés : la Précision et le Rappel.La Précision (Precision) : Sur toutes les alertes que j'ai lancées, combien étaient de vraies fraudes ?$$\text{Précision} = \frac{VP}{VP + FP}$$Le Rappel (Recall) : Sur toutes les fraudes qui existaient, combien j'en ai attrapées ?$$\text{Rappel} = \frac{VP}{VP + FN}$$Le calcul du F1-Score :$$F1 = 2 \times \frac{\text{Précision} \times \text{Rappel}}{\text{Précision} + \text{Rappel}}$$Pourquoi c'est utile ? Si tu décides de ne rien prédire comme fraude, ton Rappel tombe à 0. Si tu prédis que tout est une fraude, ta Précision tombe proche de 0. Le F1-Score te force à être bon sur les deux tableaux.3. Le PR AUC (Precision-Recall Area Under the Curve)C'est souvent la métrique la plus robuste pour ton cas (déséquilibre extrême).Un modèle ne donne pas juste "Oui" ou "Non", il donne une probabilité (ex: 0.85 de chance que ce soit une fraude). Pour décider si c'est une fraude, tu choisis un seuil (par défaut 0.5).Si tu baisses le seuil (ex: 0.1), tu attrapes plus de fraudeurs (Rappel monte), mais tu bloques plein d'innocents (Précision baisse).Si tu montes le seuil (ex: 0.9), tu ne bloques que les cas ultra-certains (Précision haute), mais tu rates beaucoup de fraudeurs (Rappel baisse).Le calcul du PR AUC :On fait varier le seuil de 0 à 1.Pour chaque seuil, on calcule la Précision et le Rappel.On trace une courbe avec le Rappel en X et la Précision en Y.L'AUC (Aire sous la courbe) est la surface totale sous cette ligne. Plus elle est proche de 1, plus ton modèle est performant.


Pour le projet utiliser: PR AUC (Precision-Recall Area Under the Curve)

