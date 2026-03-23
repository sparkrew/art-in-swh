var cols, rows;
var w = 25;
var grid = [];
var stack = [];
var current;

function setup()
{
    createCanvas(500,500);
    cols = floor(width/w);
    rows = floor(height/w);
    //frameRate();
    console.log(frameRate());

    for(var j = 0; j < rows; j++)
    {
        for(var i = 0; i < cols; i++)
        {
            var cell = new Cell(i,j);
            grid.push(cell);
        }
    }
    current = grid[0];
}

function draw()
{
    background(51);
    for(var i = 0; i < grid.length; i++)
    {
        grid[i].show();
    }
    current.visited = true;
    current.highlight();
    var next = current.getNeighbours();
    if(next)
    {
        next.visited = true;
        stack.push(current);
        current.p = true;

        removeWalls(current, next);

        current = next;
    }
    else if(stack.length > 0)
    {
        current = stack.pop();
        current.p = false;
    }
    else
    {
        console.log("Done");
        noLoop();
        return;
    }
}



function index(i, j)
{
    if(i< 0 || j < 0 || i > cols - 1 || j > rows - 1 )
        return -1;

    return i + j * cols;
}

function removeWalls(a, b)
{
    var d = a.i - b.i;
    if(d === 1)
    {
        a.walls[3] = false;
        b.walls[1] = false;
    }else if(d === -1)
    {
        a.walls[1] = false;
        b.walls[3] = false;
    }
    var c = a.j - b.j;
    if(c === -1)
    {
        a.walls[2] = false;
        b.walls[0] = false;
    }else if(c === 1)
    {
        a.walls[0] = false;
        b.walls[2] = false;
    }
}


















