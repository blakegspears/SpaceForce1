#SpaceForce

This is the flowchart for the game SpaceForce.

'''mermaid
flowchart TD
    A[Intro Screen] -->|Press S to Start| B[Main Game Loop]
    A -->|Press Q to Quit| F[Quit Game]
    B --> C[Move Spaceship]
    B --> D[Shoot Bullets]
    B --> E[Spawn Enemies]
    E --> G[Collision Detection]
    G -->|Bullet Hits Enemy| H[Update Scores]
    G -->|Player Hit| I[Game Over Screen]
    I -->|Press R to Restart| B
    I -->|Quit| F
