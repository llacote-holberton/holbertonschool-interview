#!/usr/bin/node


// Grabbing the "request engine" and setting it as a constant.
const request = require('request');

/**
 * Script's "orchestration function"
 *
 */
function main()
{
  // Exit if script not correctly runned
  if (!validArguments()) process.exit(1);

  movie_id = Number(process.argv[2]);
  printMovieCharactersNames(movie_id);
  // @warning CANNOT BE PUT HERE because exits before asynchronous calls can complete.
  // process.exit(0);
  // Would need to be put right after the character names printing. But useless because
  // NodeJS knows when and how to close program automatically.
}


/**
 * Just ensures that the script was given valid arguments to work.
 * @returns {Boolean} valid
 */
function validArguments() 
{
  // @warning whether runned "directly" or with "node myscript" syntax,
  // Arg 0 is the interpreter and arg 1 is the script's path, always.
  if (process.argv.length < 3)
  {
    const msg__error__arg_missing = 'Argument "movie id" (integer) is missing, cannot proceed!';
    console.error(msg__error__arg_missing);
    return false;
  }
  // Trying to convert as a Number directly when reading string input
  movie_id = Number(process.argv[2]);
  console.log(movie_id)
  // Using builtin "is not a number after trying to convert" method of Number class
  if (Number.isNaN(movie_id) || movie_id < 1)
  {
    const msg__error__arg_not_exploitable_int = 'Movie id must be > 0 integer!';
    console.error(msg__error__arg_not_exploitable_int)
    return false;
  }
  return true;
}


/**
 * Prints the list of character names if movie exists
 * Returns Undefined if movie not found.
 * @param {Number} movie_id
 * @returns Array[Number]|Undefined
 */
function printMovieCharactersNames(movie_id)
{
  // @note: going for simplicity, setting the separating / statically in components strings.
  const api_root_url = 'https://swapi-api.hbtn.io/api/';
  const movies_endpoint = 'films/';
  const characters_endpoint = 'characters/';
  const movie_request_url = api_root_url + movies_endpoint + movie_id;

  names_print_workflow = request
  (
    movie_request_url,
    function(error, response, body) 
    {
      // Error param is null if everything went well "in terms of network transaction"
      // (so a response with 404 HTTP code is still a valid response -> 'null error')
      if (error)
      {
        console.error("Request couldn't be processed properly.")
        return;
      }

      response_http_code = Number(response.statusCode);
      console.log(response_http_code);
      if (response_http_code != 200)
      {
        reportMovieRequestError(response_http_code);
        return;
      }

      // We can "chain" the json.parse() method returning a plain Object
      //   with the '.attribute_name' syntax. Provided of course attribute exists!
      // @note: Node 10.4 does NOT support "optional chaining syntax" ('object?.attribute')
      characters_endpoints = JSON.parse(response.body).characters;

      // Initializing the array which will store character names,
      //   keeping same "ordered by API character id"
      characters_names = [];
      // Thanks to IA, could have never understood by myself we needed to use a counter
      //   to have "control on when to print"
      number_of_requests = characters_endpoints.length;
      counter = 0;
      // @note: loops on Arrays are made by using builtin forEach, with two variants
      //   first parameter is mandatory, name given to the *value* of each array item.
      //   second parameter is *optional* and used to also get the index of currently read item.
      // CANNOT WORK
      // characters_endpoints.forEach((endpoint, index) => characters_names[index] = getCharacterName(endpoint))
      characters_endpoints.forEach
      (
        (endpoint, index) => 
        {
          getCharacterName
          (
            endpoint, 
            index, 
            (char_idx, char_name) => 
            {
              // If unsuccessful we know we return null for name
              if (char_name) characters_names[char_idx] = char_name;
              //console.log(char_name)
              // Whether successful or not we must count the achieved request
              counter++;
              // Kinda brutal but works: this is evaluated on each loop call
              // but will only print once the last request has finished.
              if (counter === number_of_requests) characters_names.forEach(name => console.log(name))
            }
          )
        }
      )
    }
  );
}

function reportMovieRequestError(http_code)
{
  if (http_code === 404) console.log("Movie not found")
  else console.log("Some internal error occured on API side");
}

/**
 * @param {String} character_endpoint
 * @returns {String} character_name
 * @note: MUST be written "as a function with callback" because otherwise
 *   it would just immediately return "undefined" to the caller because
 *   getCharacterName called synchronously but making an asynchronous call within.
 *   ALSO WHY I must also give the 'index' as parameter (otherwise that info is "lost in time")
 */
function getCharacterName(character_endpoint, index, characterNamesFillerCallback)
{
    characterNameRequest = request
    (
      character_endpoint,
      function (error, response, body)
      {
        // This time we start with 'exploitable response'
        if (!error && response.statusCode === 200) { character_name = JSON.parse(response.body).name; }
        else { character_name = null; }
        characterNamesFillerCallback(index, character_name)
      }
      
    )
}



main();


/* ========== BUSINESS GOAL ==========
 * Write a script that prints all characters of a Star Wars movie:
 * - The first positional argument passed is the Movie ID 
 *     example: 3 = "Return of the Jedi"
 * - Display one character name per line, in the same order as
 *     the "characters" list in the /films/ endpoint
 * - You must use the Star wars API
 * - You must use the request module
 */

/* ========== BRAINSTORM =========
 * 1/ CALL ARGUMENt Management
 *    a) Must read the arguments from CLI call 
 *       => How to?
 *    b) Must validate argument is exploitable (int, >0?)
 * 2/ MAKE REQUEST(s)
 *    a) Will need two levels of request, a single one to get films
 *       and drill to "characters" JSON sub-structure
 *    b) Will need to loop over the retrieved list to...
 *       - Make a subrequest on "people" API endpoint
 *       - Extract the name.
 *       - Print it
 *    => How to make a request?
 *    => How to print on standard output?
 */


/** 

/* ========== RESOURCES ==========
 * 1/ REQUESTS:
 *   https://www.npmjs.com/package/request
 * 2/ ARGUMENTS
 *   https://nodejs.org/docs/latest-v10.x/api/process.html#process_process_argv
 * 3/ PRINTING TO STD OUTPUT
 *   https://nodejs.org/learn/command-line/output-to-the-command-line-using-nodejs
 *   https://dustinpfister.github.io/2021/03/18/nodejs-process-stdout/
 *   Main differences: no automatic EOL (process.write)
 *                     automatic obj to text conversion (console.log)
 */



/*
 * ========== DRAFT / ABANDONED CODE ==========
 * function getCharacterName(character_endpoint, index, characterNamesFillerCallback)
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
         characterNamesFillerCallback(index, null)
      }
      
    )
}*


UNUSED because useless we have to "nest" calls whatever happens.
 * Grabs the list of characters from movie id.
 * Returns Undefined if movie not found.
 * @param {Number} movie_id
 * @returns Array[Number]|Undefined
function getMovieCharacters(movie_id){}

 */
