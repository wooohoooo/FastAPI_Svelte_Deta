<script>
  import { Router, Route } from "svelte-navigator";
  import Home from "./Home.svelte";
  import Experiment from "./Experiment.svelte";
  import Viz from "./Viz.svelte";


  import { onMount } from "svelte";


let sponge = '';

  onMount(async () => {

let res = await fetch('/sponge');
sponge = await res.json();
});
console.log(sponge)

$: conversation = [];
onMount(async () => {
let res = await fetch('/fake_chat');
conversation = await res.json();
});




	function addConversation() {
		conversation = [...conversation, {'role':'test','message':'test'}];
	}


let question = 'Please explain something interesting from the documents to me.'

  async function getAnswer() {

		const res = await fetch("/ask_question", {
			method: 'POST',
            headers: {"Content-type": "application/json;charset=UTF-8"},
			body: JSON.stringify({"question":question,"role":"user"})
		})

		const result = await res.json()
        conversation = [...{'role':'user', 'message':question}, result, conversation];

	}


</script>

        <div class="text-box-user">

<p></p>
<textarea bind:value={question} />
<p></p>
<button on:click={getAnswer}>
    Answer

</button>
        </div>


<span>
    <p></p>
      {#each conversation as msg, i}
        {#if msg.role == 'user'}

        <p align="left"><b>{msg.role} </b></p>
        <p align="left">{@html msg.message}</p>
        {:else if msg.role=='assistant'}
            <div class="text-box-assistant">

        <p align="left"><b>{msg.role} </b></p>
        <p align="left" background-color="#blue" display="inline-block">{@html msg.message}</p>
            </div>
        {:else}
        <p align="center"><b>{msg.role} </b></p>
        <p align="center">{@html msg.message}</p>
        {/if}
      {/each}
    <p></p>
</span>


<style>


    :root {
    --color-bg: #fafafa;
    --p0: #63678B;
    --p1: #6a84f1f2;
    --z0:#2B2E4A;
    --z1: #515368;
    --z2: #7C7D83;
    --r0: #996262;
    --r1: #B84444;
  }

  :global(.header-text) {
    color: var(--z0);
  }
  :global(.body-text) {
    color: var(--z1);
  }
  :global(.sec-text) {
    color: var(--z2);
  }
  :global(button) {
    padding: 0rem 0.5rem 0rem;
    width: 120px;
    height: 40px;
    border-radius: 4px;
    font-size: 24px;
    align-self: center;
    border: 1px solid var(--p0);
    background-color: #ffffff;
    color: var(--z2);
  }
  :global(button:hover) {
    cursor: pointer;
    border: 1px solid var(--p1);
    color: var(--p1);
  }
  :global(button:focus) {
    cursor: pointer;
    border: 1px solid var(--p1);
    color: var(--p1);
  }
  :global(select) {
    border-radius: 5px;
    background: #ffffff;
    color: var(--z0);
    border: 1px solid var(--p0);
  }
  :global(.link) {
    font-size: 14px;
    font-weight: 400;
    color: var(--p1);
    text-decoration: none;
  }
  :global(.link:hover) {
    cursor: pointer;
    text-decoration: underline;
  }
  :global(.loading) {
    font-size: 24px;
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
  }
  :global(.code) {
    font-family: monospace;
    background-color: #ffffff;
    border: 1px solid var(--p0);
    color: var(--z2);
    box-sizing: border-box;
    border-radius: 5px;
  }
  :global(.code:focus) {
    border: 1px solid var(--p1);
    color: var(--z0);
  }
  :global(.code:focus-within) {
    border: 1px solid var(--p1);
    color: var(--z0);
  }

	textarea {
		width: 100%;
		height: 100px;
	}
	div.text-box-user {
		align: left;

 width: 100%;
 padding: 10px;
 border: 5px solid gray;
 margin: 0;
}

	div.text-box-assistant {
	align: right;
 width: 100%;
 padding: 10px;
 border: 5px solid gray;
 margin: 0;
}

</style>