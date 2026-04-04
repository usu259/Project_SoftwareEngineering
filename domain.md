```mermaid
classDiagram
  direction TB

  %% =========================================================================
  %% DOMAIN LAYER
  %% =========================================================================

  class Customer {

  }

  class WorkReport {

  }

  class Position {

  }

  class StemItem {
    <<abstract>>

  }

  class MaterialItem {

  }

  class PersonnelRate {

  }

  class Invoice {

  }


  %% Domain relationships
  Customer "1" --> "*" WorkReport : has reports
  Customer "1" --> "*" Invoice : billed via
  WorkReport "1" *-- "1..*" Position : contains
  Invoice "1" o-- "1..*" WorkReport : aggregates
  Position "*" --> "0..1" StemItem : references
  StemItem <|-- MaterialItem
  StemItem <|-- PersonnelRate
  Position --> PositionType