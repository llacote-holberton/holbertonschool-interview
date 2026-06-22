



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


