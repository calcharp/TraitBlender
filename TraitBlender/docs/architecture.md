# TraitBlender Architecture

This document provides a high-level overview of TraitBlender's architecture, showing how the major systems interact and how data flows through the add-on. For detailed information about specific systems, see the [For Developers](./developers.md) documentation.

---

## System Overview

TraitBlender is organized into several interconnected systems:

```mermaid
flowchart LR
    subgraph col1[" "]
        direction TB
        UITitle["User Interface (UI)"]
        subgraph UI[" "]
            direction TB
            Operators[Operators]
            Panels[Panels]
            Properties[Properties]
            Events[Events]
            Operators ~~~ Panels
            Panels ~~~ Properties
            Properties ~~~ Events
        end
        UITitle ~~~ UI
    end
    
    subgraph col2[" "]
        direction TB
        CoreTitle["Core Systems"]
        subgraph Core[" "]
            direction TB
            Config[Configuration System]
            Transform[Transform Pipeline]
            Dataset[Dataset Management]
            Morphospace[Morphospace System]
            Positioning[Positioning System]
            Assets[Asset Management]
            Config ~~~ Transform
            Transform ~~~ Dataset
            Dataset ~~~ Morphospace
            Morphospace ~~~ Positioning
            Positioning ~~~ Assets
        end
        CoreTitle ~~~ Core
    end
    
    subgraph col3[" "]
        direction TB
        BlenderTitle["Blender Integration"]
        subgraph Blender[" "]
            direction TB
            SceneObjects[Scene Objects]
            PropertyGroups[Property Groups]
            CustomProps[Custom Properties]
            SceneObjects ~~~ PropertyGroups
            PropertyGroups ~~~ CustomProps
        end
        BlenderTitle ~~~ Blender
    end
    
    col1 --> col2
    col2 --> col3
    
    click Operators "/TraitBlender/developers/operators/" "Developer Documentation: Operators"
    click Panels "/TraitBlender/developers/panels/" "Developer Documentation: Panels"
    click Properties "/TraitBlender/developers/properties/" "Developer Documentation: Properties"
    click Events "/TraitBlender/developers/events/" "Developer Documentation: Events"
    click Config "/TraitBlender/developers/configuration-system/" "Developer Documentation: Configuration System"
    click Transform "/TraitBlender/developers/transform-pipeline/" "Developer Documentation: Transform Pipeline"
    click Dataset "/TraitBlender/developers/dataset-management/" "Developer Documentation: Dataset Management"
    click Morphospace "/TraitBlender/developers/morphospace-system/" "Developer Documentation: Morphospace System"
    click Positioning "/TraitBlender/developers/positioning-system/" "Developer Documentation: Positioning System"
    click Assets "/TraitBlender/developers/asset-management/" "Developer Documentation: Asset Management"
    click SceneObjects "/TraitBlender/developers/scene-objects/" "Developer Documentation: Scene Objects"
    click PropertyGroups "/TraitBlender/developers/property-groups/" "Developer Documentation: Property Groups"
    click CustomProps "/TraitBlender/developers/custom-properties/" "Developer Documentation: Custom Properties"
    
    style UITitle fill:transparent,stroke:transparent,font-weight:bold
    style CoreTitle fill:transparent,stroke:transparent,font-weight:bold
    style BlenderTitle fill:transparent,stroke:transparent,font-weight:bold
    style col1 fill:transparent,stroke:transparent
    style col2 fill:transparent,stroke:transparent
    style col3 fill:transparent,stroke:transparent
    style UI fill:transparent,stroke:#666
    style Core fill:transparent,stroke:#666
    style Blender fill:transparent,stroke:#666
```

