# Agents & Decisions: presenter script

Slides 1–15 form the main talk, approximately 14 minutes with code walkthrough pauses. Slides 16–21 are optional reference material. Slide 11 shows image evidence. Reference links in the slide notes are not spoken.

## Slide 1: Agents & Decisions

*30 seconds suggested*

Hi everyone. Today I’ll introduce two OpenAI platform capabilities: Agents and Decisions. We’ll look at what each one does, when to use it, and enough Python to make a first request. We’ll also cover the different ways to configure agents, and how to retrieve an agent or a session later. The agent examples are general. For Decisions, we’ll use single-value and multi-value CVL fields in PIM to make the difference between choices and predicates concrete. Toward the end, I’ll mention other possible applications. The main session takes about fourteen minutes, and the appendix provides extra code to review afterward.

## Slide 2: A task and a judgment

*45 seconds suggested*

Let’s start with the distinction we’ll use throughout the session. An agent works toward a goal. For example, it could investigate a support issue by checking information through approved tools and preparing a response. Decisions evaluates a narrower question, such as which queue should receive that issue. Think of the railway switch here as a routing judgment: it selects a direction, while a separate system carries out the work. We can use either capability independently, or combine them. The choice depends on whether we need a bounded judgment or a task that unfolds over several steps.

## Slide 3: The building blocks of an agent

*60 seconds suggested*

Before the code, four terms will help. Configuration describes the model, its instructions, and the tools it can use. A session holds a particular conversation and its work. An environment supplies compute when a task needs commands or files. Events let us observe progress and results. The managed Agents API runs the harness, which coordinates the model and tool loop. We still need to supply meaningful tools and application rules. As an example, a coding task benefits from a sandbox, while an agent using remote service tools might not need its own compute environment.

## Slide 4: Ways to create and configure agents

*60 seconds suggested*

There are three approaches to distinguish. With inline configuration, we supply settings when creating a managed session. With a saved agent, we create reusable settings once and reference the returned ID in later sessions. A compatible saved-agent ID from the Platform can serve the same referencing role, but we don’t need a dashboard setup step for these examples. Finally, the separate Agents SDK uses Agent and Runner inside our application. That object is different from a saved Agents API resource. If you encounter an Agent Builder workflow ID, check its integration instructions rather than treating it as an agent ID.

## Slide 5: Shared Python setup

*60 seconds suggested*

Here is the shared setup for the Python examples. The client reads our key from the root environment file. Notice that the two model names have different reasons behind them. We use GPT-6 Luna for Decisions because it is currently the only model supported by that endpoint. It is an API requirement today. For the agent, I chose GPT-6 Astra to match OpenAI's Agents API quickstart and use a model with strong reasoning and coding capabilities. It is a demonstration choice, not an Agents API requirement. Calculating this average does not need a flagship model. For production, evaluate supported models on your own tasks and choose a balance of quality, latency and cost. EVIDENCE supplies the navy jacket description for our CVL questions; TASK supplies the coding exercise. Install the two packages shown below, and give the project key the required permissions. Running these examples incurs usage charges.

## Slide 6: Inline agent: start a task and stream events

*75 seconds suggested*

This is an inline managed agent. We supply its model and instructions directly in the session request. The hosted environment gives it somewhere to write and run Python, and TASK contains the job we defined earlier. Hosted compute adds a separate container charge, covered in the appendix. Streaming lets us see progress as work happens. Inside the loop, we print the full JSON event, rather than only its type. The result collector then gives us final text and a session ID. We should keep that ID if we want to inspect or continue this work. The reported answer is useful, but actual tool records provide the evidence that the code ran.

## Slide 7: Saved agent: create once and reuse

*60 seconds suggested*

Now we separate configuration from a particular task. We give the saved agent a human-readable name, Technical explainer. The name helps people recognize it, while the returned agent ID is what our application stores and uses for retrieval and new sessions. The first call creates those reusable settings. The second starts a session using the ID. Here we only need an explanation, so we choose no execution environment. In production, keep creation in a deployment step and store the ID in application configuration. Another Python worker can then reuse it. Each session has its own conversation. Updating saved settings affects future sessions. An existing unnamed agent can be renamed through the update endpoint, as shown in the notebook.

## Slide 8: Retrieve an agent and a session later

*75 seconds suggested*

This answers a common persistence question: yes, another Python process can retrieve these resources later. We store the IDs, construct a client with appropriate project access, and retrieve the agent or session. Retrieving the agent tells us about its configuration. Retrieving the session tells us the state of that particular conversation, including whether it is idle, working, waiting for an action, or failed. Retrieval does not submit a new task. To inspect saved messages and tool activity, we use the session’s items endpoint, shown in the appendix. Keeping the IDs in our database connects remote work to an application job.

## Slide 9: Decisions: three bounded answer types

*75 seconds suggested*

A key benefit is speed: OpenAI describes typed answers as about ten times faster than the Responses API. That is a provider-reported comparison, not guaranteed latency for every input. We should benchmark our own workload. We’ll illustrate Decisions using CVLs, or controlled vocabulary lists, in PIM. In our example, base color accepts one allowed key, while activities accepts several. A predicate can ask whether the supplier explicitly supports hiking. A choice can map navy blue to the allowed base-color key blue. We’ll look at those two patterns next. Score is different: it rates against ordered levels. For the review, “Easy to use. I love it,” we could define zero as negative, one as neutral, and two as positive. An illustrative score of 1.8 is near the positive end. It is a position on that scale, not a CVL assignment or a confidence percentage.

## Slide 10: Single CVL: select one base_color key

*75 seconds suggested*

Here is a single-value CVL example. Our fictional base-color field allows blue, red and green. The supplier says navy blue, so the question explicitly maps navy to the canonical key blue. The API chooses one supplied option. We also include needs_review as a workflow fallback for unclear evidence. That fallback is not a valid color key and must never be written into the CVL field. After checking the answer type and excluding the fallback, we print a draft field value. In a real integration, use your PIM’s approved keys or IDs and validate the result before applying it. This code does not update the PIM.

## Slide 11: Single CVL: use a photo as evidence

*60 seconds suggested*

We can also use a photo as the evidence for a CVL decision. Here we read the supplied jacket image, encode its bytes, and create a PNG data URL. The request places that URL in an input_image part of a user message. Our choice question then selects from approved color keys, with a review fallback. For this orange jacket, orange is the illustrative draft value. We print the actual response and would apply the same refusal and fallback checks as on the previous slide before using it. A publicly accessible image URL is another option. The photo can support a visible color judgment, but it cannot establish waterproofing or certification.

## Slide 12: Multi-CVL: assess each allowed activity

*60 seconds suggested*

Now the activities field accepts several CVL keys. Its allowed keys are hiking, running and cycling. The supplier explicitly lists hiking and cycling, so those are the values we would expect in the draft. We ask one predicate for each candidate, all against the same source evidence, and assemble the array in application code. We do not treat the alternatives in a single choice question as independent labels. Refusals and intermediate probabilities go to review here. The thresholds are illustrative, and production code should check that every requested key received an answer. This JSON is draft data: adapt the write format and validation to your PIM’s API.

## Slide 13: Choosing the right amount of automation

*45 seconds suggested*

We do not need to put an agent around every model call. Exact checks are often best handled with ordinary code. Decisions is useful when interpretation leads to a bounded answer. An agent makes sense when a task needs several steps or tool use. The application still owns authorization and verification. As a possible design, Decisions could identify a request that needs investigation, and an agent could gather information and prepare a draft. For production, I would version the configuration, track each job’s session ID, and check actual outcomes rather than relying only on a convincing final response.

## Slide 14: Use cases across different systems

*60 seconds suggested*

These ideas apply across systems. In support, Decisions can select a queue while an agent investigates evidence available through approved tools. In operations, a bounded judgment can prioritize an alert, while an agent prepares a report. PIM is another example rather than the focus of this session. We could suggest product categories, identify conflicting claims, or draft supported content changes. For instance, a title that says waterproof may conflict with a supplier specification that says water resistant. The organization still needs evidence and review before accepting a factual change. The earlier photo is illustrative and cannot substantiate the claim.

## Slide 15: What to try after this session

*30 seconds suggested*

To try this afterward, I suggest two small exercises. First, take a recurring classification question and define the evidence and allowed answers for Decisions. Second, create an agent session for a small task, watch its events, and retrieve the session later using its ID. That will make the distinction between reusable settings and ongoing work much clearer. Keep the first experiments small and compare their results with what a person expects. The appendix has extra examples for the separate Agents SDK, Azure Decisions, and session inspection. That’s the main session, and I’m happy to take questions.

## Slide 16: Reference: predicate and score code

*Optional reference*

This optional example gives the score illustration from slide nine its own code. We use a customer review as the input, separately from the supplier description. One question asks whether the review is positive, while the other scores it on negative, neutral and positive levels. The numeric indices are zero, one and two, and the score may fall between them. The main CVL examples use a choice for one value and predicates for multiple values. A score instead summarizes position on an ordered scale. Printing the full response lets us inspect the actual distributions and any refusal rather than treating the illustrative value on the slide as a measured result.

## Slide 17: Reference: the separate Agents SDK

*Optional reference*

This is the separate Agents SDK version of a small example. We install openai-agents, define an Agent, and call Runner. In a notebook, top-level await avoids trying to start another event loop. The important distinction is where the runtime lives: here it runs inside our application. Constructing this object does not create a reusable server-side agent for the managed Agents API. If we want conversation state across SDK runs, we configure the SDK’s session or storage mechanism. Both approaches can be useful, but we should choose the runtime deliberately and keep their persistence models clear.

## Slide 18: Reference: Decisions through Azure

*Optional reference*

If our organization uses Azure OpenAI, this shows the Decisions client configuration. We supply the Azure resource endpoint and its credentials, then use the deployment name of a gpt-6-luna model. That deployment name may differ from the underlying model name. Here the predicate checks whether hiking is supported for the activities CVL. The request still contains supplier evidence and a typed question. We need to confirm regional availability, because feature rollout can vary. Microsoft’s current guide excludes East US 2. This Azure example establishes Decisions usage only. It does not mean the managed Agents API examples can use the same Azure endpoint. Keep the two client configurations separate.

## Slide 19: Reference: saved work and session cleanup

*Optional reference*

Here we inspect the work saved in a session. We first retrieve its state, then list items such as messages and tool activity. That helps us check what actually happened, especially after a stream disconnects. Before starting another session as a retry, inspect the existing one so we do not accidentally duplicate the job. The final line shows deletion, but it is commented out deliberately. We should save any required artifacts before cleaning up. A session ID is useful for follow-up and investigation, but our application should also record which user, tenant or job owns it.

## Slide 20: OpenAI-hosted environment costs

*Optional reference*

Here is the cost model for an OpenAI-hosted environment. There are separate charges for model tokens, the container, and any priced tools. The published container table lists three cents for small, twelve cents for medium, and forty-eight cents for large per twenty-minute container session. Eligible sessions instead have per-minute billing with a five-minute minimum, so confirm which treatment applies. Our code omits size and therefore uses medium by default. For a lightweight exercise, we can select small explicitly. When finished, save needed files and delete the session to request cleanup. Simply closing the stream does not cancel the task.

## Slide 21: Official references and hands-on practice

*Optional reference*

These are the resources I would use to continue learning. For Agents, begin with the overview and quickstart, then read configuration and retrieval. For Decisions, start with the guide and experiment with the different question types. Try changing one input at a time so you can see how the behavior changes. Our companion notebook contains a PIM-themed lab if that domain is useful, but the API patterns apply more generally. When we move beyond learning, the next step is to evaluate realistic examples and add application error handling, permissions and lifecycle management.
