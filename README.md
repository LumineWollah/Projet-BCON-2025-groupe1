# Projet-BCON-2025

🛣️ Feuille de route - Auto Compo Lite



🎯 **Objectif principal**

  Créer un addon léger, simple et pédagogique qui applique automatiquement des effets de compositing (glare, vignette, color balance), tout en étant facilement extensible pour les utilisateurs plus avancés.

✅ **Phase 1** : Prototype Minimal Viable (MVP) (mai - juin 2025)

 
 

🔹 **Interface simple**      

Panneau dans Render Properties avec un bouton "Appliquer Auto Compo"   ✅ Fait

🔹 **Setup de nodes**   

Glare + Vignette + Color Balance enchaînés automatiquement              ✅ Fait

🔹 **Sauvegarde de preset** 

Créer une version simple avec les réglages "hardcodés" pour débutants   ✅ Fait




🚀 **Phase 2**: Expériences utilisateur et ajout d’options (juillet 2025)


🔸 **Options dans l’UI**

Checkbox : Activer/Désactiver Glare, Vignette, Color Correction

🔸 **Application automatique**

Ajout d’un flag : “Appliquer automatiquement au rendu”

🔸 **Compatibilité AgX**

Ajuster les nodes pour un meilleur rendu sous AgX (Color Space aware)




💡 **Phase 3** : Fonctionnalités avancées & différenciation (août - septembre 2025)

🧠 **Scène-aware**

Analyser la lumière/contraste pour adapter l’intensité des effets (jour/nuit, intérieur/extérieur)

🧩 **Mode pédagogique**

Tooltip ou mini popup expliquant chaque effet

🔁 **Presets custom**

Sauvegarde et chargement de presets utilisateurs (via JSON)




🌍 **Phase 4** : Préparation à la présentation Blender Conference (octobre 2025)


🎥 **Vidéo démo**

Courte vidéo montrant l’avant/après d’un rendu avec Auto Compo Lite

🗣 **Présentation**

Slides + explication des choix UX/dev

📦 **Publication**

Release sur Blender Market ou [GitHub + Gumroad/Itch.io]




🧩 **Bonus / Idées futures**

Intégration au Video Sequence Editor (effets sur montage)


Live preview en viewport avec Real-Time Compositor


API pour d’autres addons/plugins


Prise en charge de Cryptomatte ou Z-pass auto




📝 **Présentation**



🎯 **Titre (Title)**

  Auto Compo Lite : Simplifier le compositing dans Blender

  

📄 **Résumé**

  Auto Compo Lite est un addon léger pour Blender qui configure automatiquement les effets de lueur (glare), de vignettage et de correction des couleurs dans le compositeur. Cette présentation explore sa conception, ses objectifs et la manière dont il aide les artistes à améliorer rapidement leurs rendus sans nécessiter une expertise approfondie des nœuds.

  
  
💡 **Proposition de projet**

  Auto Compo Lite est un addon léger pour Blender, conçu pour automatiser les effets de base en compositing (glare, vignette, correction des couleurs), afin d’aider les artistes à améliorer rapidement leurs rendus, sans devoir manipuler de nœuds complexes.
  
Le problème rencontré par les artistes est que  le compositing dans Blender est puissant mais intimidant, surtout pour les débutants.
Notre solution : Un bouton unique dans l’interface qui applique automatiquement une configuration de nœuds prête à l’emploi, sans effort.
