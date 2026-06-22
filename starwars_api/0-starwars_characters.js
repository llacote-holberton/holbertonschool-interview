#!/usr/bin/node
// Script printing the names of Star Wars characters for a given movie.
// For details confer Instructions section in README.

// Grabbing the "request engine" and setting it as a constant.
const request = require('request');
main();

/**
 * Script's "orchestration function"
 *
 */
function main()
{
  if (!validArguments()) process.exit(1);

  const movie_id = Number(process.argv[2]);
  printMovieCharactersNames(movie_id);
}

/**
 * Just ensures that the script was given valid arguments to work.
 * @returns {Boolean} valid
 */
function validArguments()
{
  if (process.argv.length < 3)
  {
    const msg__error__arg_missing = 'Argument "movie id" (integer) is missing, cannot proceed!';
    console.error(msg__error__arg_missing);
    return false;
  }
  const movie_id = Number(process.argv[2]);
  if (Number.isNaN(movie_id) || movie_id < 1)
  {
    const msg__error__arg_not_exploitable_int = 'Movie id must be > 0 integer!';
    console.error(msg__error__arg_not_exploitable_int);
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
  const movie_request_url = api_root_url + movies_endpoint + movie_id;

  request
  (
    movie_request_url,
    function(error, response, body)
    {
      if (error)
      {
        console.error("Request couldn't be processed properly.");
        return;
      }

      const response_http_code = Number(response.statusCode);
      if (response_http_code != 200)
      {
        reportMovieRequestError(response_http_code);
        return;
      }

      const characters_endpoints = JSON.parse(response.body).characters;

      // Using temporary variables to control when and how print names.
      const characters_names = [];
      const number_of_requests = characters_endpoints.length;
      let counter = 0;

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
              // Condition still useful to avoid printing "null" lines.
              if (char_name) characters_names[char_idx] = char_name;
              counter++;
              // Condition required to delay printing until all requests finished.
              if (counter === number_of_requests) characters_names.forEach(name => console.log(name));
            }
          )
        }
      )
    }
  );
}

function reportMovieRequestError(http_code)
{
  if (http_code === 404) console.log('Movie not found');
  else console.log('Some internal error occured on API side');
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
    request
    (
      character_endpoint,
      function (error, response, body)
      {
        if (!error && response.statusCode === 200) { character_name = JSON.parse(response.body).name; }
        else { character_name = null; }
        characterNamesFillerCallback(index, character_name);
      }
      
    )
}
