
// Grabbing the "request engine" and setting it as a constant.
const request = require('request');

my_test_request = request(
    // First parameter is the url of the page we want to reach
    'https://www.york.ac.uk/teaching/cws/wws/webpage1.html',
    // Second parameter is an "anonymous function" which can do
    //   different things depending on what was received in return
    //   (valid answer or HTTP error code)
    // WARNING: you can give whatever names but the order IS IMPOSED
    //   as request() will always return these informations like this.
    function (error, response, body ) 
    {
        console.log(error);
        console.log(response.statusCode);
    }
)


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


