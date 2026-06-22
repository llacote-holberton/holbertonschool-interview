# Developer's Notes

This document centralizes all information related to how this mini-program was designed and written.
Made by using AI to detect and moves all comments in code, then adjusted manually as needed.

## Business Goal

Confer [Instructions section in README](./README.md#instructions)

## Exploration

### Brainstorm

1/ CALL ARGUMENT Management  

a) Must read the arguments from CLI call  
=> How to? 

b) Must validate argument is exploitable (int, >0?) 

2/ MAKE REQUEST(s) 

a) Will need two levels of request, a single one to get films and drill to "characters" JSON sub-structure 

b) Will need to loop over the retrieved list to... - Make a subrequest on "people" API endpoint - Extract the name. - Print it  
=> How to make a request?  
=> How to print on standard output?

### Resources

1. REQUESTS: <https://www.npmjs.com/package/request> 
2. ARGUMENTS <https://nodejs.org/docs/latest-v10.x/api/process.html#process_process_argv> 
3. PRINTING TO STD OUTPUT
* <https://nodejs.org/learn/command-line/output-to-the-command-line-using-nodejs> 
* <https://dustinpfister.github.io/2021/03/18/nodejs-process-stdout/> 

Main differences: no automatic EOL (process.write) automatic obj to text conversion (console.log)

## Design notes

### Architecture Decision Records

**Global & Imports**

-   Grabbing the "request engine" (`request`) and setting it as a constant since it's kinda a "request factory".

**`main()` - Orchestration**

-   Exits early if the script is not correctly run.

-   **Self-Learning Note (`process.exit`)**: A `process.exit(0)` CANNOT be put at the end of the `main()` function because it would exit the script immediately before any asynchronous calls can complete. It would technically need to be placed right after the character names printing. However, it is actually useless to add it, because NodeJS automatically knows when and how to close the program once the event loop is empty.

**`validArguments()` - Input Validation**

-   Ensures that the script was given valid arguments to work.

-   **Warning on Arguments**: Whether run "directly" or with the `node myscript` syntax, Argument `0` is the interpreter and Argument `1` is the script's path, always. The actual user inputs start at index `2`.

-   Tries to convert the string input directly to a `Number`, using the built-in `Number.isNaN()` method of the `Number` class to verify if it is an exploitable integer.

**`printMovieCharactersNames()` - Core Logic**

-   **URL Construction**: Going for simplicity, setting the separating `/` statically in component strings.

-   **Network Errors vs HTTP Errors**: The `error` parameter from the request module is `null` if everything went well "in terms of network transaction". Therefore, a response with a 404 HTTP code is still a valid response and results in a `null` network error.

-   **JSON Parsing**: We can "chain" the `JSON.parse()` method (which returns a plain Object) with the `.attribute_name` syntax, provided the attribute actually exists.

-   **Compatibility Note**: Node 10.4 does NOT support "optional chaining syntax" (`object?.attribute`).

-   **Array Mutation**: Initializing the array which will store character names, keeping the same order as the API character IDs. It feels counterintuitive, but because an Array is an Object, we can *mutate its content* even if it is declared with `const`. `const` just prevents assigning a completely new Object to the same variable name.

-   **Asynchronous Loop Control**: Discovered that a simple iteration (like `characters_endpoints.forEach((endpoint, index) => characters_names[index] = getCharacterName(endpoint))`) CANNOT WORK. We absolutely need to use a counter to have control over when to trigger the final print.

-   **Array `forEach` Iteration**: Loops on Arrays are made using the built-in `forEach`, with two variants. The first parameter is mandatory (the name given to the *value* of each array item). The second parameter is *optional* and used to get the *index* of the currently read item.

-   **Completion Checking**: The logic evaluates the counter on *each loop call* (when a response arrives) and increments it whether the request is successful or not. It's kinda brutal but works perfectly: it will only execute the final print loop once the last request has finished.

**`getCharacterName()` - API Sub-requests**

-   **Self-Learning Note (Callbacks & Async Execution)**: This MUST be written as a "function with callback". Otherwise, it would immediately return `undefined` to the caller because `getCharacterName` is executed synchronously while making an asynchronous call within it.

-   **Passing the Index**: This asynchronous behavior is ALSO WHY the `index` must be passed as a parameter directly to the function. Otherwise, that positional information is "lost in time" when the callback eventually fires.

-   In the updated workflow, we start by checking for an 'exploitable response' (`!error && response.statusCode === 200`). If unsuccessful, we explicitly return `null` for the name to avoid polluting the final array.

### Prototypes / Abandoned code

**Abandoned Prototype 1: Direct Error Handling inside the Callback** *Explanation for abandonment:* This implementation had a logical flaw leading to double callback executions (alternating `null` and actual names) because the `characterNamesFillerCallback(index, null)` was executed outside of the `else` block.

JavaScript

```
function getCharacterName(character_endpoint, index, characterNamesFillerCallback)
{
    console.log(character_endpoint);
    characterNameRequest = request
    (
      character_endpoint,
      function (error, response, body)
      {
        // This time we start with 'exploitable response'
        if (!error && response.statusCode === 200)
        {
          character_name = JSON.parse(response.body).name;
          characterNamesFillerCallback(index, character_name)
        }
        else
        {
          if (error) console.error("Request couldn't be processed properly.");
          else if (response.statusCode === 404)
          {
            console.log(`Character does not exist for endpoint ${character_endpoint}`)
          }
          else console.error('Some error happened on API server side')
        }
        // BUG: This fires every time, even on success!
        characterNamesFillerCallback(index, null)
      }

    )
}

```

**Abandoned Prototype 2: Modularized "Get Movies" function** *Explanation for abandonment:* Unused because it was ultimately useless. Due to the asynchronous nature of the `request` module in Node 10.4, we have to "nest" the calls (or use callbacks) whatever happens, making a separate synchronous-looking wrapper ineffective.

JavaScript

```
/**
 * Grabs the list of characters from movie id.
 * Returns Undefined if movie not found.
 * @param {Number} movie_id
 * @returns Array[Number]|Undefined
 */
function getMovieCharacters(movie_id){}
```
