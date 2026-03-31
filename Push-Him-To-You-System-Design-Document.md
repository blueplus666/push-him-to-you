# "Push Him To You" - AI-Driven Fate Simulation and Novel Generation System

## Project Vision

**"Push Him To You"** is an innovative AI-driven fate simulation and novel generation system. It is not merely a writing tool, but a "life simulator" — after users set the initial conditions of characters and the world background, the system acts like a god's eye view, allowing characters to naturally grow and change based on their own characteristics and environmental factors, ultimately being pushed by fate toward their destined ending. The system automatically captures and records those shining, touching, and meaningful moments throughout life's journey.

---

## I. System Overview

### 1.1 Core Philosophy

```
Setting → Simulation → Recording → Narrative
    ↓         ↓           ↓          ↓
Initial    Life        Spark      Multi-perspective
Conditions Operation   Moments    Novel
```

### 1.2 System Features

| Feature | Description |
|---------|-------------|
| **Multi-LLM Collaboration** | Different large models each perform their own duties, simulating different dimensions of the world |
| **Dynamic Character Growth** | Based on psychological models, characters truly change due to environment and events |
| **Fate Engine** | Driven by causality rather than preset plots |
| **God's Eye View** | Observe character life trajectories, capture key moments |
| **Perspective Slicing** | Switch to any character's perspective at any time to regenerate narrative |
| **Spark Recording** | Automatically identify and save touching, meaningful moments |

---

## II. System Architecture

### 2.1 Overall Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              User Interface Layer (UI Layer)                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Settings   │ │   World     │ │    Life     │ │   Novel     │           │
│  │  Panel      │ │  Building   │ │ Observation │ │ Generation  │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Orchestration Layer                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Master Orchestrator                               │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐           │   │
│  │  │  Task     │ │  State    │ │  Conflict │ │  Result   │           │   │
│  │  │ Scheduling│ │ Management│ │ Resolution│ │Integration│           │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────┘           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Agent Layer                                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ WorldBuilder│ │CharacterGen │ │ FateEngine  │ │ Narrator    │           │
│  │   Agent     │ │   Agent     │ │   Agent     │ │   Agent     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Emotional   │ │ EventGen    │ │RelationNet  │ │SparkCapture │           │
│  │ Renderer    │ │   Agent     │ │   Agent     │ │   Agent     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Model Layer                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        LLM Gateway                                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ Claude  │ │ GPT-4   │ │ Gemini  │ │ Wenxin  │ │ Tongyi  │ ...   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Layer                                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │   Vector    │ │  Graph DB   │ │  Time-series│ │    Spark    │           │
│  │  Database   │ │  (Neo4j)    │ │  Event DB   │ │ Memory Store│           │
│  │(Milvus/     │ │             │ │ (PostgreSQL)│ │             │           │
│  │  Chroma)    │ │             │ │             │ │             │           │
│  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Core Module Description

#### 2.2.1 User Interface Layer
Provides intuitive parameter setting interface, allowing users to:
- Configure LLM API keys and model selection
- Set basic parameters for the novel world
- Create and configure characters
- Observe life simulation progress
- Select perspective to generate novels

#### 2.2.2 Orchestration Layer
As the "brain" of the system, responsible for:
- Scheduling the execution order of each Agent
- Managing global state
- Resolving conflicts between Agents
- Integrating final output

#### 2.2.3 Agent Layer
Contains multiple specialized Agents, each responsible for a specific domain:
- **WorldBuilder Agent**: Creates and maintains the story world
- **CharacterGenerator Agent**: Manages character attributes and growth
- **FateEngine Agent**: Advances causal chains
- **Narrator Agent**: Generates specific text
- **EmotionalRenderer Agent**: Adjusts narrative emotional tone
- **EventGenerator Agent**: Creates life events
- **RelationNetwork Agent**: Manages character relationships
- **SparkCapture Agent**: Identifies meaningful moments

#### 2.2.4 Model Layer
Unified LLM access gateway:
- Supports multiple LLM providers
- Automatic load balancing
- Failover mechanism
- Cost optimization strategy

#### 2.2.5 Data Layer
Multi-dimensional data storage:
- **Vector Database**: Stores semantic memories, supports similarity retrieval
- **Graph Database**: Stores character relationship networks
- **Time-series Event DB**: Stores all events by timeline
- **Spark Memory Store**: Specifically stores highlight moments

---

## III. Character Model Design

### 3.1 Big Five Personality-Based Character Attribute System

Character personality adopts the widely recognized Big Five personality model (OCEAN) in psychology as the foundation:

```
┌─────────────────────────────────────────────────────────────────┐
│                     Big Five Personality Dimensions (OCEAN)     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  O - Openness                        Range: 0-100              │
│  ├── Imagination                      Sub-dimension             │
│  ├── Aesthetics                                                 │
│  ├── Feelings                                                  │
│  ├── Actions                                                   │
│  ├── Ideas                                                     │
│  └── Values                                                    │
│                                                                 │
│  C - Conscientiousness               Range: 0-100              │
│  ├── Competence                                                │
│  ├── Order                                                     │
│  ├── Dutifulness                                               │
│  ├── Achievement                                               │
│  ├── Self-Discipline                                           │
│  └── Deliberation                                              │
│                                                                 │
│  E - Extraversion                    Range: 0-100              │
│  ├── Warmth                                                    │
│  ├── Gregariousness                                            │
│  ├── Assertiveness                                             │
│  ├── Activity                                                  │
│  ├── Excitement-Seeking                                        │
│  └── Positive Emotions                                         │
│                                                                 │
│  A - Agreeableness                   Range: 0-100              │
│  ├── Trust                                                     │
│  ├── Straightforwardness                                       │
│  ├── Altruism                                                  │
│  ├── Compliance                                                │
│  ├── Modesty                                                   │
│  └── Tender-Mindedness                                         │
│                                                                 │
│  N - Neuroticism                     Range: 0-100              │
│  ├── Anxiety                                                   │
│  ├── Angry Hostility                                           │
│  ├── Depression                                                │
│  ├── Self-Consciousness                                        │
│  ├── Impulsiveness                                             │
│  └── Vulnerability                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Complete Character Attribute Model

```json
{
  "character": {
    "id": "char_001",
    "name": "Li Ming",
    "gender": "male",
    "birth_date": "1990-03-15",
    "birth_place": {
      "province": "Zhejiang",
      "city": "Hangzhou",
      "rural_urban": "urban"
    },
    
    "personality": {
      "ocean": {
        "openness": 75,
        "conscientiousness": 68,
        "extraversion": 45,
        "agreeableness": 82,
        "neuroticism": 35
      },
      "sub_dimensions": {
        "imagination": 80,
        "aesthetics": 70,
        "trust": 85,
        "anxiety": 30
      }
    },
    
    "background": {
      "family": {
        "father_occupation": "Teacher",
        "mother_occupation": "Doctor",
        "family_economic_status": "middle",
        "family_atmosphere": "harmonious",
        "siblings": 1,
        "birth_order": 1
      },
      "education": {
        "highest_degree": "bachelor",
        "major": "Computer Science",
        "school_tier": "985"
      }
    },
    
    "current_state": {
      "age": 25,
      "occupation": "Software Engineer",
      "income_level": 4,
      "relationship_status": "single",
      "health_status": "good",
      "mental_state": "stable",
      "life_satisfaction": 72
    },
    
    "needs": {
      "physiological": 85,
      "safety": 78,
      "belonging": 65,
      "esteem": 70,
      "self_actualization": 55
    },
    
    "skills": {
      "technical": ["Programming", "Data Analysis"],
      "social": ["Communication", "Teamwork"],
      "creative": ["Writing"],
      "physical": ["Swimming", "Running"]
    },
    
    "values": {
      "core_values": ["Family", "Freedom", "Growth"],
      "life_goal": "Become a technical expert",
      "fear": "Living an ordinary life"
    },
    
    "memory_vector_id": "vec_char_001",
    "relationship_graph_id": "rel_char_001",
    "event_timeline_id": "timeline_char_001"
  }
}
```

### 3.3 Factors Affecting Character Growth

Based on psychological research and system design requirements, the following factors affect character growth, physiological, and psychological changes:

#### 3.3.1 Natural Environment Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Geographic Environment** | Birthplace urban/rural | Openness, Extraversion | Urban dwellers are typically more open and extraverted |
| | Coastal/Inland | Values, Career choices | Affects worldview and opportunity access |
| | Climate type | Emotional stability | Long-term climate affects psychological state |
| **Natural Disasters** | Earthquakes, floods, typhoons | Neuroticism, Security sense | PTSD, reduced sense of security |
| | Plagues/Epidemics | Values, Interpersonal relationships | Re-examination of life's meaning |
| **Ecological Environment** | Air quality | Health status, Emotions | Long-term impact on physical and mental health |
| | Natural landscape accessibility | Openness, Aesthetic ability | Contact with nature enhances openness |

#### 3.3.2 Socio-Political Environment Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Political Environment** | Political stability | Security sense, Planning ability | Unstable environments reduce long-term planning willingness |
| | Policy changes | Career choices, Values | Policy direction affects life choices |
| | War/Conflict | Trauma, Values | Extreme environments reshape personality |
| **Economic Environment** | Economic cycles | Conscientiousness, Anxiety | Economic recessions increase anxiety and caution |
| | Industry development | Career path, Skills | Industrial changes affect career development |
| | Job market | Confidence, Income | Affects self-efficacy |
| **Social Culture** | Cultural values | Core values, Behavioral patterns | Culture shapes personality foundation |
| | Social class mobility | Goal setting, Striving motivation | Affects expectations for the future |
| | Public opinion environment | Self-perception, Behavioral expression | Affects self-presentation style |

#### 3.3.3 Family Environment Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Family Structure** | Parents' marital status | Trust, Agreeableness | Divorced families affect intimate relationship building |
| | Number of siblings | Social skills, Sharing awareness | Affects interpersonal interaction patterns |
| | Birth order | Responsibility, Achievement motivation | Firstborns typically have more responsibility |
| **Family Economy** | Economic status | Security sense, Values | Poverty/Wealth affects resource access and values |
| | Economic changes | Coping ability, Anxiety | Sudden changes affect psychological resilience |
| **Family Education** | Parenting style | Autonomy, Social skills | Democratic/Authoritarian/Permissive have different impacts |
| | Educational expectations | Conscientiousness, Achievement motivation | High expectations may bring pressure or motivation |
| **Family Atmosphere** | Emotional atmosphere | Emotion regulation, Trust | Harmonious families cultivate security sense |
| | Conflict frequency | Neuroticism, Coping strategies | High-conflict families increase anxiety tendency |

#### 3.3.4 Educational Experience Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **School Education** | School quality | Knowledge, Skills, Values | Quality education enhances overall quality |
| | Academic performance | Confidence, Conscientiousness | Success experiences enhance self-efficacy |
| | Teacher-student relationship | Trust, Learning attitude | Good relationships promote growth |
| **Peer Influence** | Quality of friend circle | Values, Behavioral patterns | Peer groups shape behavior |
| | Social status | Self-esteem, Social skills | Affects self-perception |
| | Bullying experience | Neuroticism, Trust | Trauma affects long-term mental health |
| **Higher Education** | Major selection | Career path, Thinking style | Major shapes thinking patterns |
| | University experience | Openness, Social network | University is a key period for personality shaping |
| | Academic achievement | Confidence, Career starting point | Affects career development starting point |

#### 3.3.5 Career/Work Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Work Environment** | Work pressure | Neuroticism, Health | High-pressure work affects physical and mental health |
| | Work autonomy | Conscientiousness, Satisfaction | Autonomy affects work engagement |
| | Team atmosphere | Social skills, Belonging sense | Affects job satisfaction and growth |
| **Career Development** | Promotion opportunities | Achievement motivation, Confidence | Affects career expectations and effort |
| | Career bottleneck | Anxiety, Values | Affects career identity and transition |
| | Unemployment experience | Self-esteem, Security sense | Unemployment trauma affects long-term psychology |
| **Income Changes** | Income level | Quality of life, Security sense | Affects life choices and psychological state |
| | Income fluctuation | Anxiety, Planning ability | Unstable income increases anxiety |

#### 3.3.6 Interpersonal Relationship Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Intimate Relationships** | Dating experience | Trust, Emotion regulation | Dating shapes intimate relationship capabilities |
| | Marriage quality | Happiness, Stability | Marriage is an important support system |
| | Breakup/Divorce | Trauma, Trust | Relationship breakdown affects psychology |
| **Friendship** | Friendship quality | Belonging sense, Support system | Friends are important social support |
| | Number of friends | Social skills, Resources | Social network affects opportunity access |
| **Social Network** | Network quality | Opportunities, Information access | Affects career and life development |
| | Community belonging | Belonging sense, Security sense | Community participation affects happiness |

#### 3.3.7 Major Life Events

| Event Category | Specific Events | Affected Dimensions | Impact Mechanism |
|----------------|-----------------|---------------------|------------------|
| **Positive Events** | Marriage | Happiness, Responsibility | Life stage transition |
| | Promotion | Confidence, Achievement sense | Career identity enhancement |
| | Awards/Recognition | Self-esteem, Motivation | External recognition enhances confidence |
| **Negative Events** | Death of loved one | Trauma, Values | Re-examination of life's meaning |
| | Major illness | Values, Life attitude | Health crisis changes life perspective |
| | Bankruptcy/Debt | Anxiety, Security sense | Economic crisis affects psychology |
| **Turning Point Events** | Immigration/Relocation | Openness, Adaptability | Environmental changes promote growth |
| | Career transition | Self-perception, Skills | Career identity reshaping |
| | Entrepreneurship | Conscientiousness, Risk preference | Entrepreneurship experience shapes personality |

#### 3.3.8 Personal Internal Factors

| Factor Category | Specific Factors | Affected Dimensions | Impact Mechanism |
|----------------|------------------|---------------------|------------------|
| **Physiological Factors** | Genetic inheritance | Personality foundation | Genes affect personality tendencies |
| | Health status | Vitality, Psychological state | Health affects psychological state |
| | Appearance | Self-esteem, Social opportunities | Appearance affects social experience |
| **Psychological Factors** | Cognitive style | Decision-making patterns | Affects information processing style |
| | Emotion regulation ability | Neuroticism | Affects emotional stability |
| | Self-efficacy | Action ability, Confidence | Affects goal pursuit |
| **Will Factors** | Goal setting | Life trajectory | Goals guide behavior |
| | Self-discipline level | Conscientiousness | Affects goal achievement |
| | Resilience | Psychological toughness | Affects coping with difficulties |

### 3.4 Character Growth Dynamic Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    Character Growth Dynamic Model               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Initial State                                                 │
│      │                                                          │
│      ▼                                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │         Environmental Factor Input       │                  │
│   │  Natural + Social + Family + ...         │                  │
│   └─────────────────────────────────────────┘                  │
│                      │                                          │
│                      ▼                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │         Event Trigger Engine             │                  │
│   │  Random + Causal + Key Node Events       │                  │
│   └─────────────────────────────────────────┘                  │
│                      │                                          │
│                      ▼                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │     Personality-Event Interaction        │                  │
│   │  Personality × Event Type × Coping Style │                  │
│   │         = Psychological + Behavioral     │                  │
│   │              Changes                     │                  │
│   └─────────────────────────────────────────┘                  │
│                      │                                          │
│                      ▼                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │         State Update                     │                  │
│   │  Personality Adjustment + Need Changes   │                  │
│   │  + Relationship Changes                  │                  │
│   └─────────────────────────────────────────┘                  │
│                      │                                          │
│                      ▼                                          │
│   ┌─────────────────────────────────────────┐                  │
│   │         Spark Moment Detection           │                  │
│   │  Emotional Intensity × Significance ×    │                  │
│   │  Uniqueness > Threshold → Record as      │                  │
│   │  Spark Moment                            │                  │
│   └─────────────────────────────────────────┘                  │
│                      │                                          │
│                      ▼                                          │
│   Loop until life ends                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.4.1 Personality Change Calculation Formula

```
Personality Dimension Change = f(Current Personality, Event Intensity, Event Type, Coping Style, Time Accumulation)

Specific Calculation:
ΔP = α × E × T × R × (1 - S)

Where:
- ΔP: Personality dimension change amount
- α: Base change coefficient (usually small, like 0.01-0.05)
- E: Event intensity (1-10)
- T: Event type match degree (-1 to 1)
- R: Coping style adjustment (0.5-1.5)
- S: Personality stability coefficient (0-1, increases with age)

Example:
A person with high neuroticism (N=75) encounters unemployment (intensity 8):
- Event type: Negative stress event, positively correlated with neuroticism (T=0.8)
- Coping style: Negative coping (R=1.2)
- Age 25, stability S=0.3
- ΔN = 0.02 × 8 × 0.8 × 1.2 × (1-0.3) = 0.1075
- New N value = 75 + 0.1075 ≈ 75.11 (Small but cumulatively effective)
```

---

## IV. Multi-LLM Collaboration Mechanism

### 4.1 Agent Role Definition and Division of Labor

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Agent Collaboration Architecture       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                          │
│                    │ Master          │                          │
│                    │ Orchestrator    │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐              │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │ World Layer │     │ Character   │     │ Story Layer │       │
│  │             │     │ Layer       │     │             │       │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘       │
│         │                   │                   │              │
│    ┌────┴────┐         ┌────┴────┐         ┌────┴────┐        │
│    ▼         ▼         ▼         ▼         ▼         ▼        │
│ ┌────┐   ┌────┐    ┌────┐   ┌────┐    ┌────┐   ┌────┐        │
│ │World│   │Env.│    │Char.│   │Rel.│    │Fate│   │Narr.│        │
│ │Build│   │Sim │    │Gen  │   │Net │    │Eng.│   │Gen  │        │
│ └────┘   └────┘    └────┘   └────┘    └────┘   └────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Detailed Agent Definitions

#### 4.2.1 WorldBuilder Agent

**Responsibilities**: Create and maintain the story world's basic settings

```yaml
Agent: WorldBuilder
Role: World Architect
Primary_Model: Claude-3-Opus (Excellent at creative and structured thinking)
Backup_Model: GPT-4

Responsibilities:
  - Create world basic settings (era, location, social background)
  - Define social rules and cultural characteristics
  - Generate environment descriptions
  - Maintain world consistency

Outputs:
  - world_setting: World setting document
  - environment_state: Current environment state
  - social_rules: Social rules set

Prompt_Template: |
  You are a professional world builder. Please construct a complete story world based on the following parameters:
  
  Era background: {era}
  Geographic scope: {location}
  Society type: {society_type}
  Special settings: {special_settings}
  
  Please output:
  1. World overview (200 words)
  2. Social structure (classes, power distribution)
  3. Cultural characteristics (values, customs)
  4. Environmental features (natural, urban)
  5. Potential conflict sources (social contradictions, resource competition)
```

#### 4.2.2 CharacterGenerator Agent

**Responsibilities**: Create and manage characters, handle character growth

```yaml
Agent: CharacterGenerator
Role: Character Psychologist
Primary_Model: GPT-4 (Excellent at logical reasoning and personality analysis)
Backup_Model: Claude-3-Sonnet

Responsibilities:
  - Create character initial settings
  - Calculate personality changes
  - Handle character growth
  - Generate character behavioral decisions

Outputs:
  - character_profile: Character profile
  - personality_changes: Personality change records
  - behavioral_decisions: Behavioral decisions

Prompt_Template: |
  You are a professional psychologist and character creation expert. Please analyze the character based on the following information:
  
  Current character state:
  {character_state}
  
  Encountered event:
  {event}
  
  Environmental factors:
  {environment_factors}
  
  Please analyze:
  1. Character's psychological reaction to this event
  2. Possible behavioral choices (based on personality traits)
  3. Potential changes in personality dimensions
  4. Long-term psychological impact prediction
```

#### 4.2.3 FateEngine Agent

**Responsibilities**: Advance causal chains, generate events

```yaml
Agent: FateEngine
Role: Fate Weaver
Primary_Model: Claude-3-Opus (Excellent at complex causal reasoning)
Backup_Model: Gemini-Pro

Responsibilities:
  - Generate life events
  - Maintain causal chains
  - Identify key nodes
  - Advance fate trajectory

Outputs:
  - events: Event list
  - causal_chain: Causal chain
  - key_moments: Key moment markers
  - fate_trajectory: Fate trajectory prediction

Prompt_Template: |
  You are a fate weaver, responsible for advancing the character's life trajectory.
  
  Character's current state:
  {character_state}
  
  World environment:
  {world_state}
  
  Past events:
  {event_history}
  
  Please generate:
  1. Possible next events (3-5 candidates)
  2. Trigger conditions for each event
  3. Potential impacts of events
  4. Correlation with fate endpoint
```

#### 4.2.4 Narrator Agent

**Responsibilities**: Transform events into narrative text

```yaml
Agent: Narrator
Role: Storyteller
Primary_Model: Claude-3-Opus (Excellent at literary creation)
Backup_Model: GPT-4

Responsibilities:
  - Generate narrative text
  - Adjust narrative style
  - Handle perspective switching
  - Render emotional atmosphere

Outputs:
  - narrative_text: Narrative text
  - emotional_tone: Emotional tone
  - perspective: Narrative perspective

Prompt_Template: |
  You are a professional novelist. Please transform the following event into vivid narrative:
  
  Event:
  {event}
  
  Protagonist:
  {protagonist}
  
  Narrative perspective: {perspective}
  Emotional tone: {emotional_tone}
  Style requirements: {style}
  
  Please generate:
  1. Scene description
  2. Character's inner thoughts
  3. Dialogue (if any)
  4. Emotional rendering
```

#### 4.2.5 EmotionalRenderer Agent

**Responsibilities**: Analyze and adjust emotional tone

```yaml
Agent: EmotionalRenderer
Role: Emotional Designer
Primary_Model: Claude-3-Sonnet
Backup_Model: GPT-3.5-Turbo

Responsibilities:
  - Analyze emotional intensity
  - Adjust narrative emotion
  - Identify touching moments
  - Balance emotional rhythm

Outputs:
  - emotional_analysis: Emotional analysis
  - tone_adjustments: Tone adjustment suggestions
  - emotional_peaks: Emotional peak markers
```

#### 4.2.6 EventGenerator Agent

**Responsibilities**: Generate specific life events

```yaml
Agent: EventGenerator
Role: Event Designer
Primary_Model: GPT-4
Backup_Model: Claude-3-Haiku

Responsibilities:
  - Generate daily events
  - Generate turning point events
  - Generate random events
  - Validate event rationality

Outputs:
  - daily_events: Daily events
  - turning_points: Turning point events
  - random_events: Random events
  - event_validation: Event validation results
```

#### 4.2.7 RelationNetwork Agent

**Responsibilities**: Manage character relationship networks

```yaml
Agent: RelationNetwork
Role: Relationship Analyst
Primary_Model: GPT-4
Backup_Model: Claude-3-Sonnet

Responsibilities:
  - Establish character relationships
  - Track relationship changes
  - Analyze relationship impacts
  - Predict relationship development

Outputs:
  - relationship_graph: Relationship graph
  - relationship_changes: Relationship changes
  - influence_analysis: Influence analysis
```

#### 4.2.8 SparkCapture Agent

**Responsibilities**: Identify and record meaningful moments

```yaml
Agent: SparkCapture
Role: Spark Catcher
Primary_Model: Claude-3-Opus
Backup_Model: GPT-4

Responsibilities:
  - Evaluate event significance
  - Identify touching moments
  - Extract spark fragments
  - Generate spark tags

Outputs:
  - spark_moments: Spark moment list
  - significance_score: Significance score
  - emotional_impact: Emotional impact degree
  - spark_tags: Spark tags

Prompt_Template: |
  You are a keen life observer, responsible for identifying meaningful spark moments in life.
  
  Current event:
  {event}
  
  Character state:
  {character_state}
  
  Life background:
  {life_context}
  
  Please evaluate:
  1. Emotional intensity (1-10)
  2. Life significance (1-10)
  3. Uniqueness (1-10)
  4. Whether it's worth recording as a spark moment
  5. If yes, please provide spark tags and brief description
```

### 4.3 Agent Collaboration Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Collaboration Workflow                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Initialization Phase                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. WorldBuilder creates world settings                   │   │
│  │ 2. CharacterGenerator creates character profiles         │   │
│  │ 3. RelationNetwork initializes relationship network      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Phase 2: Simulation Loop (each time cycle)                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Loop:                                                     │   │
│  │   1. FateEngine generates candidate events               │   │
│  │   2. EventGenerator refines events                       │   │
│  │   3. CharacterGenerator calculates character reactions   │   │
│  │   4. RelationNetwork updates relationships               │   │
│  │   5. SparkCapture evaluates spark moments                │   │
│  │   6. Narrator generates narrative                        │   │
│  │   7. EmotionalRenderer adjusts emotion                   │   │
│  │   8. Store to vector database                            │   │
│  │ Until: Life ends                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  Phase 3: Novel Generation Phase                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. Select narrative perspective                          │   │
│  │ 2. Retrieve relevant memories from vector database       │   │
│  │ 3. Narrator generates complete narrative                 │   │
│  │ 4. EmotionalRenderer unifies emotional tone              │   │
│  │ 5. Output final novel                                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 Model Selection Strategy

```python
class ModelSelector:
    """
    Automatically select the optimal model based on task characteristics
    """
    
    MODEL_CAPABILITIES = {
        "claude-3-opus": {
            "creativity": 9.5,
            "logic": 9.0,
            "long_context": 9.5,
            "narrative": 9.5,
            "cost": "high"
        },
        "gpt-4": {
            "creativity": 9.0,
            "logic": 9.5,
            "long_context": 8.0,
            "narrative": 8.5,
            "cost": "high"
        },
        "claude-3-sonnet": {
            "creativity": 8.5,
            "logic": 8.5,
            "long_context": 9.0,
            "narrative": 8.0,
            "cost": "medium"
        },
        "gemini-pro": {
            "creativity": 8.0,
            "logic": 8.5,
            "long_context": 9.0,
            "narrative": 7.5,
            "cost": "medium"
        }
    }
    
    def select_model(self, task_type: str, requirements: dict) -> str:
        """
        Task type -> Optimal model selection
        """
        task_model_mapping = {
            "world_building": "claude-3-opus",  # Needs creativity and structure
            "character_creation": "gpt-4",       # Needs logical reasoning
            "event_generation": "gpt-4",         # Needs causal reasoning
            "narrative_writing": "claude-3-opus", # Needs literary creation
            "emotional_analysis": "claude-3-sonnet", # Balance cost-performance
            "relationship_tracking": "gpt-4",    # Needs logical analysis
            "spark_detection": "claude-3-opus",  # Needs deep understanding
        }
        
        return task_model_mapping.get(task_type, "claude-3-sonnet")
```

---

## V. Fate Engine Design

### 5.1 Fate Engine Core Concepts

The fate engine is the core of the system, responsible for advancing the character's life trajectory. It is not a preset plot, but dynamically generates based on causal relationships.

```
┌─────────────────────────────────────────────────────────────────┐
│                      Fate Engine Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                 Causal Chain Manager                      │  │
│   │  ┌─────────┐   ┌─────────┐   ┌─────────┐               │  │
│   │  │ Cause A │ → │ Result B│ → │Effect C │ ...           │  │
│   │  └─────────┘   └─────────┘   └─────────┘               │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Event Generator                        │  │
│   │  ┌───────────────┐  ┌───────────────┐                  │  │
│   │  │ Deterministic │  │   Random      │                  │  │
│   │  │    Events     │  │   Events      │                  │  │
│   │  │ (Causal-driven)│ │(Probability-  │                  │  │
│   │  │               │  │   driven)     │                  │  │
│   │  └───────────────┘  └───────────────┘                  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                Key Node Identifier                        │  │
│   │  Detect: Life turning points, fate branching points,     │  │
│   │         endpoint approaching signals                      │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │               Fate Endpoint Manager                       │  │
│   │  Maintain: Preset endpoint vs Dynamic endpoint           │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Event Type System

```yaml
Event_Types:
  
  Life_Stage_Events:
    description: "Life stage events - inevitable life nodes"
    examples:
      - Birth
      - School enrollment
      - Graduation
      - Employment
      - Marriage
      - Retirement
      - Death
    trigger: "Time-driven"
    flexibility: "Low - Basically inevitable, but specific form can vary"
  
  Causal_Events:
    description: "Causal events - triggered by previous events"
    examples:
      - Studying hard → Getting into a good university
      - Introverted personality → Missing social opportunities
      - Investment failure → Financial difficulties
    trigger: "Causal chain driven"
    flexibility: "Medium - Depends on antecedent causes"
  
  Random_Events:
    description: "Random events - probabilistic occurrence"
    categories:
      Positive:
        - Winning lottery
        - Meeting a benefactor
        - Unexpected opportunity
      Negative:
        - Accidents
        - Illness
        - Natural disasters
      Neutral:
        - Chance encounters
        - Environmental changes
    trigger: "Probability-driven"
    flexibility: "High - Completely random"
  
  Character_Driven_Events:
    description: "Character-driven events - triggered by personality traits"
    examples:
      - High conscientiousness → Voluntary overtime
      - High neuroticism → Excessive worry leading to insomnia
      - High openness → Trying new things
    trigger: "Personality trait driven"
    flexibility: "Medium - Personality determines tendency"
  
  Relationship_Events:
    description: "Relationship events - triggered by interpersonal relationships"
    examples:
      - Friend introduces job
      - Family member falls ill
      - Lover breaks up
    trigger: "Relationship network driven"
    flexibility: "Medium - Relationships determine probability"
  
  Environment_Events:
    description: "Environment events - triggered by external environment"
    examples:
      - Economic crisis
      - Policy changes
      - Social unrest
    trigger: "Environmental state driven"
    flexibility: "Low - Environment determines"
```

### 5.3 Event Generation Algorithm

```python
class EventGenerator:
    """
    Event Generator - Generates life events by integrating multiple factors
    """
    
    def generate_next_event(self, character, world_state, event_history):
        """
        Generate the next event
        """
        candidates = []
        
        # 1. Check life stage events
        stage_events = self.check_life_stage_events(character.age)
        candidates.extend(stage_events)
        
        # 2. Check causal chain events
        causal_events = self.check_causal_chain(event_history)
        candidates.extend(causal_events)
        
        # 3. Generate random events
        random_events = self.generate_random_events(
            character, 
            world_state,
            probability_threshold=0.1
        )
        candidates.extend(random_events)
        
        # 4. Generate character-driven events
        character_events = self.generate_character_driven_events(character)
        candidates.extend(character_events)
        
        # 5. Generate relationship events
        relationship_events = self.generate_relationship_events(character)
        candidates.extend(relationship_events)
        
        # 6. Generate environment events
        environment_events = self.generate_environment_events(world_state)
        candidates.extend(environment_events)
        
        # 7. Select final event
        selected_event = self.select_event(candidates, character, world_state)
        
        return selected_event
    
    def select_event(self, candidates, character, world_state):
        """
        Select the final event from candidates
        Consider: Priority, probability, fate trajectory
        """
        # Sort by priority
        priority_order = {
            "life_stage": 1,      # Highest priority
            "causal": 2,
            "environment": 3,
            "relationship": 4,
            "character_driven": 5,
            "random": 6           # Lowest priority
        }
        
        # Calculate comprehensive score for each event
        scored_events = []
        for event in candidates:
            score = self.calculate_event_score(event, character, world_state)
            scored_events.append((event, score))
        
        # Select highest scoring event
        scored_events.sort(key=lambda x: x[1], reverse=True)
        return scored_events[0][0]
    
    def calculate_event_score(self, event, character, world_state):
        """
        Calculate event score
        """
        score = 0
        
        # Priority weight
        priority_weight = {
            "life_stage": 100,
            "causal": 80,
            "environment": 60,
            "relationship": 50,
            "character_driven": 40,
            "random": 20
        }
        score += priority_weight.get(event.type, 0)
        
        # Fate relevance
        fate_relevance = self.calculate_fate_relevance(event, character.fate_endpoint)
        score += fate_relevance * 30
        
        # Character fit
        character_fit = self.calculate_character_fit(event, character.personality)
        score += character_fit * 20
        
        # Time validity
        time_validity = self.check_time_validity(event, character.age)
        score += time_validity * 10
        
        return score
```

### 5.4 Fate Endpoint Management

```python
class FateEndpointManager:
    """
    Fate Endpoint Manager
    """
    
    def __init__(self, initial_endpoint=None):
        self.initial_endpoint = initial_endpoint  # User preset endpoint
        self.dynamic_endpoint = None              # Dynamically evolved endpoint
        self.endpoint_type = "preset" if initial_endpoint else "dynamic"
    
    def determine_endpoint(self, character, event_history):
        """
        Determine fate endpoint
        """
        if self.endpoint_type == "preset":
            # Preset endpoint mode: Advance toward preset endpoint
            return self.initial_endpoint
        else:
            # Dynamic endpoint mode: Naturally evolve based on life trajectory
            return self.evolve_endpoint(character, event_history)
    
    def evolve_endpoint(self, character, event_history):
        """
        Dynamically evolve endpoint
        Judge possible ending based on character personality, choices, environment
        """
        # Analyze life trajectory trend
        trajectory = self.analyze_trajectory(event_history)
        
        # Predict possible ending types
        possible_endings = self.predict_endings(character, trajectory)
        
        # Select most likely ending
        most_likely_ending = self.select_most_likely(possible_endings)
        
        return most_likely_ending
    
    def check_endpoint_proximity(self, character, current_state):
        """
        Check if approaching fate endpoint
        """
        proximity_signals = []
        
        # Age signal
        if character.age > 70:
            proximity_signals.append(("age", 0.8))
        
        # Health signal
        if current_state.health_status == "critical":
            proximity_signals.append(("health", 0.9))
        
        # Life completion
        life_completion = self.calculate_life_completion(character, current_state)
        proximity_signals.append(("completion", life_completion))
        
        # Comprehensive judgment
        overall_proximity = sum(s[1] for s in proximity_signals) / len(proximity_signals)
        
        return overall_proximity
```

---

## VI. Perspective Switching and Narrative Generation

### 6.1 Multi-Perspective Narrative System

```
┌─────────────────────────────────────────────────────────────────┐
│                    Multi-Perspective Narrative System           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Original Event Stream (God's eye view recording)              │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Event1 → Event2 → Event3 → Event4 → ... → EventN        │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              Perspective Filter                           │  │
│   │                                                          │  │
│   │  Character A perspective: [Event1, Event3, Event5, ...]  │  │
│   │  Character B perspective: [Event2, Event3, Event4, ...]  │  │
│   │  Character C perspective: [Event1, Event4, Event6, ...]  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              Narrative Reconstructor                      │  │
│   │                                                          │  │
│   │  1. Retrieve memory vectors for this perspective         │  │
│   │  2. Reconstruct event sequence for this perspective      │  │
│   │  3. Generate psychological activities for this perspective│  │
│   │  4. Generate narrative text for this perspective         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│   Output: Complete single-perspective novel                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Perspective Switching Mechanism

```python
class PerspectiveSwitcher:
    """
    Perspective Switcher
    """
    
    def __init__(self, vector_db, event_db):
        self.vector_db = vector_db
        self.event_db = event_db
    
    def switch_perspective(self, target_character_id, original_timeline):
        """
        Switch to specified character's perspective
        """
        # 1. Get all events this character participated in
        participated_events = self.get_participated_events(
            target_character_id, 
            original_timeline
        )
        
        # 2. Retrieve this character's memory vectors
        memory_vectors = self.vector_db.query(
            collection="character_memories",
            filter={"character_id": target_character_id}
        )
        
        # 3. Reconstruct event sequence for this perspective
        perspective_events = self.reconstruct_perspective(
            participated_events,
            memory_vectors
        )
        
        # 4. Generate psychological activities for this perspective
        internal_monologues = self.generate_internal_monologues(
            target_character_id,
            perspective_events
        )
        
        return {
            "character_id": target_character_id,
            "events": perspective_events,
            "memories": memory_vectors,
            "internal_monologues": internal_monologues
        }
    
    def reconstruct_perspective(self, events, memories):
        """
        Reconstruct perspective: Re-understand events from this character's angle
        """
        reconstructed = []
        
        for event in events:
            # Get this character's perception of the event
            perception = self.get_character_perception(event, memories)
            
            # Get this character's emotional reaction
            emotion = self.get_character_emotion(event, memories)
            
            # Get this character's inner thoughts
            thought = self.get_character_thought(event, memories)
            
            reconstructed.append({
                "event": event,
                "perception": perception,
                "emotion": emotion,
                "thought": thought
            })
        
        return reconstructed
```

### 6.3 Narrative Generation Process

```python
class NarrativeGenerator:
    """
    Narrative Generator
    """
    
    def generate_novel(self, perspective_data, style_config):
        """
        Generate complete novel
        """
        novel = {
            "title": "",
            "chapters": []
        }
        
        # 1. Generate title
        novel["title"] = self.generate_title(perspective_data)
        
        # 2. Divide into chapters by time
        chapters = self.divide_into_chapters(perspective_data["events"])
        
        # 3. Generate content for each chapter
        for chapter_events in chapters:
            chapter = self.generate_chapter(
                chapter_events,
                perspective_data,
                style_config
            )
            novel["chapters"].append(chapter)
        
        return novel
    
    def generate_chapter(self, events, perspective_data, style_config):
        """
        Generate single chapter content
        """
        chapter = {
            "number": events[0]["chapter_number"],
            "title": "",
            "content": ""
        }
        
        # Generate chapter title
        chapter["title"] = self.generate_chapter_title(events)
        
        # Generate chapter content
        content_parts = []
        
        for event_data in events:
            # Scene description
            scene = self.generate_scene_description(event_data, style_config)
            
            # Character action
            action = self.generate_action_description(event_data)
            
            # Inner thoughts
            internal = self.generate_internal_narrative(
                event_data["thought"],
                style_config
            )
            
            # Dialogue (if any)
            dialogue = self.generate_dialogue(event_data) if event_data.get("dialogue") else ""
            
            # Combine
            content_parts.append(self.combine_narrative_elements(
                scene, action, internal, dialogue, style_config
            ))
        
        chapter["content"] = "\n\n".join(content_parts)
        
        return chapter
```

---

## VII. Vector Database Storage Solution

### 7.1 Vector Database Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Vector Database Architecture                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Collections                            │  │
│   ├─────────────────────────────────────────────────────────┤  │
│   │                                                          │  │
│   │  ┌─────────────────┐  ┌─────────────────┐              │  │
│   │  │ character_      │  │ event_          │              │  │
│   │  │ memories        │  │ embeddings      │              │  │
│   │  └─────────────────┘  └─────────────────┘              │  │
│   │                                                          │  │
│   │  ┌─────────────────┐  ┌─────────────────┐              │  │
│   │  │ relationship_   │  │ spark_          │              │  │
│   │  │ memories        │  │ moments         │              │  │
│   │  └─────────────────┘  └─────────────────┘              │  │
│   │                                                          │  │
│   │  ┌─────────────────┐  ┌─────────────────┐              │  │
│   │  │ world_          │  │ narrative_      │              │  │
│   │  │ knowledge       │  │ fragments       │              │  │
│   │  └─────────────────┘  └─────────────────┘              │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Index Structure                        │  │
│   ├─────────────────────────────────────────────────────────┤  │
│   │  HNSW Index + Time Index + Character ID Index            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Data Model Design

#### 7.2.1 Character Memory Vector

```json
{
  "collection": "character_memories",
  "schema": {
    "id": "string (UUID)",
    "character_id": "string",
    "timestamp": "datetime",
    "age_at_event": "float",
    "event_type": "string",
    "event_summary": "string",
    "embedding": "vector[1536]",
    "metadata": {
      "emotional_intensity": "float (0-1)",
      "significance": "float (0-1)",
      "related_characters": ["string"],
      "location": "string",
      "event_id": "string"
    }
  }
}
```

#### 7.2.2 Event Embedding Vector

```json
{
  "collection": "event_embeddings",
  "schema": {
    "id": "string (UUID)",
    "event_id": "string",
    "timestamp": "datetime",
    "event_type": "string",
    "event_description": "string",
    "embedding": "vector[1536]",
    "metadata": {
      "participants": ["string"],
      "causes": ["string"],
      "effects": ["string"],
      "world_state_snapshot": "object"
    }
  }
}
```

#### 7.2.3 Spark Moment Vector

```json
{
  "collection": "spark_moments",
  "schema": {
    "id": "string (UUID)",
    "character_id": "string",
    "timestamp": "datetime",
    "spark_type": "string (emotional/meaningful/unique)",
    "description": "string",
    "embedding": "vector[1536]",
    "metadata": {
      "emotional_score": "float (0-10)",
      "meaning_score": "float (0-10)",
      "uniqueness_score": "float (0-10)",
      "tags": ["string"],
      "related_event_id": "string",
      "narrative_fragment": "string"
    }
  }
}
```

### 7.3 Vector Retrieval Strategy

```python
class VectorRetriever:
    """
    Vector Retriever
    """
    
    def __init__(self, vector_db):
        self.db = vector_db
    
    def retrieve_relevant_memories(self, query, character_id, top_k=10):
        """
        Retrieve relevant memories
        """
        # Semantic similarity retrieval
        results = self.db.query(
            collection="character_memories",
            query_vector=self.embed(query),
            filter={"character_id": character_id},
            top_k=top_k
        )
        
        return results
    
    def retrieve_by_time_range(self, character_id, start_time, end_time):
        """
        Retrieve by time range
        """
        results = self.db.query(
            collection="character_memories",
            filter={
                "character_id": character_id,
                "timestamp": {"$gte": start_time, "$lte": end_time}
            }
        )
        
        return results
    
    def retrieve_spark_moments(self, character_id, spark_type=None):
        """
        Retrieve spark moments
        """
        filter_dict = {"character_id": character_id}
        if spark_type:
            filter_dict["spark_type"] = spark_type
        
        results = self.db.query(
            collection="spark_moments",
            filter=filter_dict,
            order_by={"significance": "desc"}
        )
        
        return results
    
    def retrieve_for_narrative(self, event, perspective_character_id):
        """
        Retrieve relevant context for narrative generation
        """
        # Retrieve memories related to this event
        event_memories = self.retrieve_relevant_memories(
            event["description"],
            perspective_character_id,
            top_k=5
        )
        
        # Retrieve related character memories
        related_memories = []
        for participant in event["participants"]:
            if participant != perspective_character_id:
                memories = self.retrieve_relevant_memories(
                    event["description"],
                    participant,
                    top_k=3
                )
                related_memories.extend(memories)
        
        # Retrieve related spark moments
        sparks = self.retrieve_spark_moments(perspective_character_id)
        
        return {
            "event_memories": event_memories,
            "related_memories": related_memories,
            "spark_moments": sparks
        }
```

---

## VIII. Spark Moment Capture System

### 8.1 Spark Moment Definition

Spark moments are those instants in life worth recording and savoring. The system identifies these moments through multi-dimensional evaluation:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Spark Moment Evaluation Dimensions           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Dimension 1: Emotional Intensity                              │
│   ├── Extreme sadness (10) - Death of loved one, heartbreak     │
│   ├── Extreme joy (10) - Marriage, birth of child               │
│   ├── Deeply moved (9) - Being understood, accepted              │
│   ├── Strong anger (8) - Being betrayed, wronged                │
│   └── ...                                                       │
│                                                                 │
│   Dimension 2: Life Significance                                │
│   ├── Fate turning point (10) - Life direction change           │
│   ├── Value reshaping (9) - Worldview change                    │
│   ├── Relationship deepening (8) - Important relationship       │
│   ├── Self-breakthrough (8) - Overcoming major difficulties     │
│   └── ...                                                       │
│                                                                 │
│   Dimension 3: Uniqueness                                       │
│   ├── Life first (10) - First time...                           │
│   ├── Rare experience (9) - Few people experience                │
│   ├── Special combination (8) - Multiple factor coincidence     │
│   └── ...                                                       │
│                                                                 │
│   Dimension 4: Narrative Value                                  │
│   ├── Dramatic tension (10) - Intense conflict                  │
│   ├── Emotional resonance (9) - Easy for readers to empathize   │
│   ├── Rich imagery (8) - Strong visual sense                    │
│   └── ...                                                       │
│                                                                 │
│   Comprehensive Score = Σ(Dimension Score × Weight)             │
│   Spark Threshold = 7.0                                         │
│   If Comprehensive Score ≥ 7.0, mark as spark moment            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Spark Moment Types

```yaml
Spark_Types:
  
  Emotional_Sparks:
    description: "Emotional sparks - Intense emotional experiences"
    subtypes:
      - deep_love          # Deep love
      - heartbreak         # Heartbreak
      - overwhelming_joy   # Overwhelming joy
      - profound_grief     # Profound grief
      - unexpected_touch   # Unexpectedly touched
    example: "Waiting in the rain for three hours, just to catch a glimpse of her"
  
  Growth_Sparks:
    description: "Growth sparks - Life growth nodes"
    subtypes:
      - self_discovery     # Self-discovery
      - value_shift        # Value transformation
      - skill_mastery      # Skill breakthrough
      - perspective_change # Perspective shift
    example: "First realizing that father's white hair was caused by me"
  
  Relationship_Sparks:
    description: "Relationship sparks - Interpersonal relationship highlights"
    subtypes:
      - connection         # Soul connection
      - reconciliation     # Reconciliation
      - sacrifice          # Sacrifice
      - understanding      # Understanding
    example: "Reuniting years later, we smiled at each other, past grievances dissipated"
  
  Destiny_Sparks:
    description: "Destiny sparks - Fate turning points"
    subtypes:
      - turning_point      # Turning point
      - coincidence        # Coincidence
      - revelation         # Revelation
      - closure            # Closure
    example: "That decision changed my entire life"
  
  Beauty_Sparks:
    description: "Beauty sparks - Beauty in life"
    subtypes:
      - simple_happiness   # Simple happiness
      - quiet_moment       # Quiet moment
      - natural_beauty     # Natural beauty
      - human_warmth       # Human warmth
    example: "Sunlight fell on her profile, in that moment, the world stood still"
```

### 8.3 Spark Capture Algorithm

```python
class SparkCapture:
    """
    Spark Moment Capture
    """
    
    def __init__(self, llm_client, vector_db):
        self.llm = llm_client
        self.vector_db = vector_db
        self.threshold = 7.0
    
    def evaluate_event(self, event, character, life_context):
        """
        Evaluate whether event is a spark moment
        """
        # Calculate scores for each dimension
        emotional_score = self.calculate_emotional_intensity(event, character)
        significance_score = self.calculate_significance(event, character, life_context)
        uniqueness_score = self.calculate_uniqueness(event, character)
        narrative_score = self.calculate_narrative_value(event)
        
        # Weighted combination
        weights = {
            "emotional": 0.3,
            "significance": 0.3,
            "uniqueness": 0.2,
            "narrative": 0.2
        }
        
        total_score = (
            emotional_score * weights["emotional"] +
            significance_score * weights["significance"] +
            uniqueness_score * weights["uniqueness"] +
            narrative_score * weights["narrative"]
        )
        
        # Determine if it's a spark moment
        is_spark = total_score >= self.threshold
        
        return {
            "is_spark": is_spark,
            "total_score": total_score,
            "scores": {
                "emotional": emotional_score,
                "significance": significance_score,
                "uniqueness": uniqueness_score,
                "narrative": narrative_score
            }
        }
    
    def calculate_emotional_intensity(self, event, character):
        """
        Calculate emotional intensity
        """
        prompt = f"""
        Evaluate the emotional impact intensity of the following event on the character (1-10):
        
        Character: {character.name}
        Character personality: {character.personality_summary}
        Event: {event.description}
        
        Please provide emotional intensity rating and reasoning.
        """
        
        response = self.llm.generate(prompt)
        return self.parse_score(response)
    
    def calculate_significance(self, event, character, life_context):
        """
        Calculate life significance
        """
        prompt = f"""
        Evaluate the significance of the following event to the character's life (1-10):
        
        Character: {character.name}
        Life stage: {character.age} years old
        Life background: {life_context}
        Event: {event.description}
        
        Consider:
        1. Does it change life direction
        2. Does it affect values
        3. Does it affect important relationships
        
        Please provide significance rating and reasoning.
        """
        
        response = self.llm.generate(prompt)
        return self.parse_score(response)
    
    def capture_spark(self, event, character, evaluation):
        """
        Capture and store spark moment
        """
        if not evaluation["is_spark"]:
            return None
        
        # Generate spark description
        spark_description = self.generate_spark_description(event, character)
        
        # Generate narrative fragment
        narrative_fragment = self.generate_narrative_fragment(event, character)
        
        # Determine spark type
        spark_type = self.determine_spark_type(event, evaluation)
        
        # Generate tags
        tags = self.generate_tags(event, character, evaluation)
        
        # Store to vector database
        spark_record = {
            "character_id": character.id,
            "timestamp": event.timestamp,
            "spark_type": spark_type,
            "description": spark_description,
            "embedding": self.embed(spark_description),
            "metadata": {
                "emotional_score": evaluation["scores"]["emotional"],
                "meaning_score": evaluation["scores"]["significance"],
                "uniqueness_score": evaluation["scores"]["uniqueness"],
                "tags": tags,
                "related_event_id": event.id,
                "narrative_fragment": narrative_fragment
            }
        }
        
        self.vector_db.insert("spark_moments", spark_record)
        
        return spark_record
```

---

## IX. User Interface Design

### 9.1 Interface Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    "Push Him To You" Main Interface             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Navigation Bar                                          │   │
│  │  [Settings] [World Building] [Character Creation]        │   │
│  │  [Life Simulation] [Novel Generation]                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │                     Main Content Area                    │   │
│  │                                                          │   │
│  │  Display different modules based on current navigation:  │   │
│  │  - Settings: API configuration, model selection          │   │
│  │  - World Building: Era, location, social settings        │   │
│  │  - Character Creation: Character attribute settings      │   │
│  │  - Life Simulation: Real-time observation of life        │   │
│  │  - Novel Generation: Perspective selection, novel output │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Status Bar                                              │   │
│  │  Current Model: Claude-3-Opus | Progress: 25 years |     │   │
│  │  Status: Running                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Core Function Modules

#### 9.2.1 Settings Module

```
┌─────────────────────────────────────────────────────────────────┐
│  API Settings                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Model Provider Configuration                            │   │
│  │                                                          │   │
│  │  [+] Add New Model                                       │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ Claude (Anthropic)                     [Connected]│   │   │
│  │  │ API Key: sk-ant-****                            │    │   │
│  │  │ Default Model: claude-3-opus                     │    │   │
│  │  │ Status: ● Normal                                 │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                                                          │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ OpenAI                                 [Connected]│   │   │
│  │  │ API Key: sk-****                                │    │   │
│  │  │ Default Model: gpt-4                             │    │   │
│  │  │ Status: ● Normal                                 │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Model Assignment Strategy                               │   │
│  │                                                          │   │
│  │  World Building: [Claude-3-Opus ▼]                       │   │
│  │  Character Creation: [GPT-4 ▼]                           │   │
│  │  Narrative Generation: [Claude-3-Opus ▼]                 │   │
│  │  Emotional Analysis: [Claude-3-Sonnet ▼]                 │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.2.2 World Building Module

```
┌─────────────────────────────────────────────────────────────────┐
│  World Building                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Basic Settings                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Era Background: [Modern Urban ▼]                        │   │
│  │  Geographic Scope: [China ▼] [Zhejiang ▼] [Hangzhou ▼]  │   │
│  │  Time Span: From [1990] to [2025]                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Social Settings                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Society Type: [Steady Development ▼]                    │   │
│  │  Economic Environment: [Moderately Developed ▼]          │   │
│  │  Cultural Atmosphere: [Traditional-Modern Fusion ▼]      │   │
│  │                                                          │   │
│  │  Special Settings:                                        │   │
│  │  [✓] Include major social events (e.g., pandemic,        │   │
│  │      economic crisis)                                     │   │
│  │  [✓] Include natural disasters                           │   │
│  │  [ ] Include war/conflict                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Generate World Settings]                                      │
│                                                                 │
│  Preview                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  World Overview:                                          │   │
│  │  This is a story set in Hangzhou, China from 1990-2025...│   │
│  │  ...                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.2.3 Character Creation Module

```
┌─────────────────────────────────────────────────────────────────┐
│  Character Creation                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────┐  ┌─────────────────────────────────┐ │
│  │  Character List      │  │  Character Details               │ │
│  │                      │  │                                  │ │
│  │  [+] Add Character   │  │  Name: [Li Ming        ]        │ │
│  │                      │  │  Gender: [Male ▼]               │ │
│  │  ● Li Ming (Protagonist)│ │ Birth: [1990] Year [3] Month [15] Day │
│  │  ○ Wang Fang         │  │                                  │ │
│  │  ○ Zhang Wei         │  │  ─────────────────────────────  │ │
│  │                      │  │  Personality Traits (Big Five)  │ │
│  │                      │  │                                  │ │
│  │                      │  │  Openness:   [══════════░] 75    │ │
│  │                      │  │  Conscientiousness: [════════░░░] 68 │
│  │                      │  │  Extraversion: [══════░░░░░] 45  │ │
│  │                      │  │  Agreeableness: [══════════░] 82 │ │
│  │                      │  │  Neuroticism: [══════░░░░░] 35   │ │
│  │                      │  │                                  │ │
│  │                      │  │  ─────────────────────────────  │ │
│  │                      │  │  Family Background              │ │
│  │                      │  │  Father's Occupation: [Teacher ▼] │
│  │                      │  │  Mother's Occupation: [Doctor ▼] │
│  │                      │  │  Family Economy: [Middle ▼]     │ │
│  │                      │  │                                  │ │
│  └──────────────────────┘  └─────────────────────────────────┘ │
│                                                                 │
│  [Save Character] [Random Generate] [Import from Template]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.2.4 Life Simulation Module

```
┌─────────────────────────────────────────────────────────────────┐
│  Life Simulation - God's Eye View                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Control Panel                                           │   │
│  │  [▶ Start] [⏸ Pause] [⏹ Stop] Speed: [1x ▼]            │   │
│  │  Current Time: June 2015  Character Age: 25 years       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Event Stream                                            │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ June 2015                                         │    │   │
│  │  │                                                   │    │   │
│  │  │ 📅 Li Ming graduated from Zhejiang University    │    │   │
│  │  │    Computer Science Department                    │    │   │
│  │  │    Emotion: Joy mixed with confusion              │    │   │
│  │  │    Significance: Important life turning point     │    │   │
│  │  │    ⭐ Spark Moment (Score: 7.5)                   │    │   │
│  │  │                                                   │    │   │
│  │  │ 📅 Li Ming joined Alibaba as software engineer    │    │   │
│  │  │    Emotion: Excitement and anticipation           │    │   │
│  │  │                                                   │    │   │
│  │  │ 📅 Li Ming met Wang Fang at team building event   │    │   │
│  │  │    Emotion: Curiosity and fondness                │    │   │
│  │  │    ⭐ Spark Moment (Score: 7.2)                   │    │   │
│  │  │                                                   │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌───────────────────┐  ┌───────────────────────────────────┐ │
│  │  Character Status │  │  Spark Moment Records              │ │
│  │                   │  │                                   │ │
│  │  Li Ming (25 y/o) │  │  ⭐ Graduation Moment (7.5)        │ │
│  │  Status: Working  │  │  ⭐ Meeting Wang Fang (7.2)        │ │
│  │  Mood: Fulfilled  │  │  ⭐ ...                            │ │
│  │                   │  │                                   │ │
│  │  Personality Chg: │  │  [View All Spark Moments]          │ │
│  │  Conscientiousness│  │                                   │ │
│  │    +2             │  │                                   │ │
│  │  Openness +1      │  │                                   │ │
│  │                   │  │                                   │ │
│  └───────────────────┘  └───────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 9.2.5 Novel Generation Module

```
┌─────────────────────────────────────────────────────────────────┐
│  Novel Generation                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Perspective Selection                                   │   │
│  │                                                          │   │
│  │  Select Narrative Perspective:                           │   │
│  │  ○ Li Ming (Protagonist) - First Person                  │   │
│  │  ○ Wang Fang - First Person                              │   │
│  │  ○ Omniscient View - Third Person                        │   │
│  │                                                          │   │
│  │  Narrative Style: [Literary Realism ▼]                   │   │
│  │  Emotional Tone: [Warm and Healing ▼]                    │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Content Filtering                                       │   │
│  │                                                          │   │
│  │  [✓] Include all spark moments                           │   │
│  │  [✓] Include important life nodes                        │   │
│  │  [ ] Include daily trivia                                │   │
│  │                                                          │   │
│  │  Time Range: [Entire Life ▼]                             │   │
│  │  Focus Chapters: [Romance Line ▼]                        │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Generate Novel]                                               │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Novel Preview                                           │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │  "Push Him To You"                                │    │   │
│  │  │                                                   │    │   │
│  │  │  Chapter 1: The Summer of Graduation              │    │   │
│  │  │                                                   │    │   │
│  │  │  In June, Hangzhou, the air filled with the       │    │   │
│  │  │  scent of osmanthus...                            │    │   │
│  │  │  ...                                              │    │   │
│  │  │                                                   │    │   │
│  │  │  Chapter 2: Entering the Workplace                │    │   │
│  │  │  ...                                              │    │   │
│  │  │                                                   │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  │                                                          │   │
│  │  [Export TXT] [Export EPUB] [Export PDF]                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## X. Technical Implementation Recommendations

### 10.1 Technology Stack Selection

```yaml
Frontend:
  framework: "React + TypeScript"
  ui_library: "Ant Design / shadcn/ui"
  state_management: "Zustand"
  visualization: "D3.js (relationship graphs), ECharts (data visualization)"

Backend:
  framework: "Python + FastAPI"
  task_queue: "Celery + Redis"
  caching: "Redis"
  
AI/ML:
  llm_gateway: "LiteLLM (unified LLM interface)"
  embedding: "OpenAI text-embedding-3-small / BGE"
  vector_db: "Milvus / Chroma"
  
Database:
  primary: "PostgreSQL"
  graph: "Neo4j (relationship network)"
  time_series: "TimescaleDB (event timeline)"
  
Infrastructure:
  containerization: "Docker + Docker Compose"
  orchestration: "Kubernetes (optional)"
  monitoring: "Prometheus + Grafana"
```

### 10.2 Project Structure

```
push-him-to-you/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Settings/
│   │   │   ├── WorldBuilder/
│   │   │   ├── CharacterCreator/
│   │   │   ├── LifeSimulator/
│   │   │   └── NovelGenerator/
│   │   ├── stores/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── agents/
│   │   │   ├── world_builder.py
│   │   │   ├── character_generator.py
│   │   │   ├── fate_engine.py
│   │   │   ├── narrator.py
│   │   │   ├── emotional_renderer.py
│   │   │   ├── event_generator.py
│   │   │   ├── relation_network.py
│   │   │   └── spark_capture.py
│   │   ├── core/
│   │   │   ├── orchestrator.py
│   │   │   ├── model_selector.py
│   │   │   └── config.py
│   │   ├── models/
│   │   ├── services/
│   │   │   ├── llm_gateway.py
│   │   │   ├── vector_store.py
│   │   │   └── graph_store.py
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
│
├── docs/
│   └── Push-Him-To-You-System-Design-Document.md
│
├── docker-compose.yml
└── README.md
```

### 10.3 API Design Example

```python
# API Route Design

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# ========== Model Management ==========

class ModelConfig(BaseModel):
    provider: str
    api_key: str
    default_model: str
    alias: Optional[str] = None

@router.post("/api/models")
async def add_model(config: ModelConfig):
    """Add LLM model configuration"""
    pass

@router.get("/api/models")
async def list_models():
    """List all configured models"""
    pass

# ========== World Building ==========

class WorldConfig(BaseModel):
    era: str
    location: dict
    time_span: dict
    society_type: str
    special_settings: List[str]

@router.post("/api/worlds")
async def create_world(config: WorldConfig):
    """Create story world"""
    pass

@router.get("/api/worlds/{world_id}")
async def get_world(world_id: str):
    """Get world details"""
    pass

# ========== Character Management ==========

class CharacterConfig(BaseModel):
    name: str
    gender: str
    birth_date: str
    personality: dict
    background: dict

@router.post("/api/characters")
async def create_character(config: CharacterConfig):
    """Create character"""
    pass

@router.get("/api/characters/{character_id}")
async def get_character(character_id: str):
    """Get character details"""
    pass

# ========== Life Simulation ==========

class SimulationConfig(BaseModel):
    world_id: str
    character_ids: List[str]
    speed: float = 1.0

@router.post("/api/simulations")
async def start_simulation(config: SimulationConfig):
    """Start life simulation"""
    pass

@router.get("/api/simulations/{sim_id}/events")
async def get_simulation_events(sim_id: str, limit: int = 50):
    """Get simulation event stream"""
    pass

@router.get("/api/simulations/{sim_id}/sparks")
async def get_spark_moments(sim_id: str):
    """Get spark moments"""
    pass

# ========== Novel Generation ==========

class NovelConfig(BaseModel):
    simulation_id: str
    perspective: str
    style: str
    emotional_tone: str
    time_range: Optional[dict] = None

@router.post("/api/novels")
async def generate_novel(config: NovelConfig):
    """Generate novel"""
    pass

@router.get("/api/novels/{novel_id}")
async def get_novel(novel_id: str):
    """Get generated novel"""
    pass

@router.get("/api/novels/{novel_id}/export")
async def export_novel(novel_id: str, format: str = "txt"):
    """Export novel"""
    pass
```

---

## XI. Extensions and Future Planning

### 11.1 Short-term Extensions (v1.1)

- [ ] Support more LLM providers
- [ ] Add character relationship visualization
- [ ] Support multi-language narrative
- [ ] Add life retrospective functionality
- [ ] Support custom event templates

### 11.2 Medium-term Planning (v2.0)

- [ ] Multi-character parallel simulation
- [ ] Complex relationship network evolution
- [ ] Social group simulation
- [ ] Historical event integration
- [ ] User intervention mechanism

### 11.3 Long-term Vision (v3.0)

- [ ] Multi-world cross-narrative
- [ ] AI-assisted creative suggestions
- [ ] Community sharing platform
- [ ] Interactive novel generation
- [ ] VR/AR immersive experience

---

## XII. Summary

"Push Him To You" is an innovative project that integrates psychology, narratology, artificial intelligence, and game design. It is not just a novel generation tool, but a "life simulator" — allowing users to observe, record, and understand a person's complete journey from birth to fate's endpoint.

### Core Innovations

1. **Dynamic Character Growth**: Based on psychological models, characters truly change due to environment and events
2. **Fate Engine**: Driven by causality rather than preset plots
3. **Multi-LLM Collaboration**: Different models each perform their own duties, simulating different dimensions of the world
4. **Spark Capture**: Automatically identifies meaningful moments in life
5. **Perspective Slicing**: Switch to any character's perspective at any time to regenerate narrative

### Project Value

- **Creative Value**: Provides inspiration and material for writers
- **Educational Value**: Helps understand the relationship between life choices and fate
- **Research Value**: Provides a platform for narrative AI and personality psychology research
- **Emotional Value**: Records and shares those spark moments in life

---

*"Fate is not a preset script, but a trajectory woven from countless choices. We are merely observers, recording the most shining moments in the journey toward the endpoint."*

---

**Document Version**: v1.0  
**Creation Date**: 2026-03-31  
**Author**: AI Design Team
