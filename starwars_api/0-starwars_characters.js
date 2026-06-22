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

  const movieId = Number(process.argv[2]);
  printMovieCharactersNames(movieId);
}

/**
 * Just ensures that the script was given valid arguments to work.
 * @returns {Boolean} valid
 */
function validArguments()
{
  if (process.argv.length < 3)
  {
    const msgErrorArgMissing = 'Argument "movie id" (integer) is missing, cannot proceed!';
    console.error(msgErrorArgMissing);
    return false;
  }
  const movieId = Number(process.argv[2]);
  if (Number.isNaN(movieId) || movieId < 1)
  {
    const msgErrorArgUnexploitableInt = 'Movie id must be > 0 integer!';
    console.error(msgErrorArgUnexploitableInt);
    return false;
  }
  return true;
}


/**
 * Prints the list of character names if movie exists
 * Returns Undefined if movie not found.
 * @param {Number} movieId
 * @returns Array[Number]|Undefined
 */
function printMovieCharactersNames(movieId)
{
  // @note: going for simplicity, setting the separating / statically in components strings.
  const apiRootUrl = 'https://swapi-api.hbtn.io/api/';
  const moviesEndpoint = 'films/';
  const movieRequestUrl = apiRootUrl + moviesEndpoint + movieId;

  request
  (
    movieRequestUrl,
    function(error, response, body)
    {
      if (error)
      {
        console.error("Request couldn't be processed properly.");
        return;
      }

      const responseHttpCode = Number(response.statusCode);
      if (responseHttpCode != 200)
      {
        reportMovieRequestError(responseHttpCode);
        return;
      }

      const charactersEndpoints = JSON.parse(response.body).characters;

      // Using temporary variables to control when and how print names.
      const charactersNames = [];
      const requestsToMakeCount = charactersEndpoints.length;
      let counter = 0;

      charactersEndpoints.forEach((endpoint, index) => {
          getCharacterName( endpoint, index, (charIdx, charName) => {
              // Condition still useful to avoid printing "null" lines.
              if (charName) charactersNames[charIdx] = charName;
              counter++;
              // Condition required to delay printing until all requests finished.
              if (counter === requestsToMakeCount) charactersNames.forEach(name => console.log(name));
            }
          )
        }
      )
    }
  );
}

function reportMovieRequestError(httpCode)
{
  if (httpCode === 404) console.log('Movie not found');
  else console.log('Some internal error occured on API side');
}

/**
 * @param {String} characterEndpoint
 * @returns {String} characterName
 * @note: MUST be written "as a function with callback" because otherwise
 *   it would just immediately return "undefined" to the caller because
 *   getCharacterName called synchronously but making an asynchronous call within.
 *   ALSO WHY I must also give the 'index' as parameter (otherwise that info is "lost in time")
 */
function getCharacterName(characterEndpoint, index, characterNamesFillerCallback)
{
    request
    (
      characterEndpoint,
      function (error, response, body)
      {
        if (!error && response.statusCode === 200) { characterName = JSON.parse(response.body).name; }
        else { characterName = null; }
        characterNamesFillerCallback(index, characterName);
      }
      
    )
}
