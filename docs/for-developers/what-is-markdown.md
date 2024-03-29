<style>
  /* This is a hack. Don't do this. TOC gets generated by H tags, so we gotta impersonate. */
  .as-h1 { color: var(--md-default-fg-color--light); font-size: 2em; line-height: 1.3; margin: 0 0 1.25em; }
  .as-h2 { font-size: 1.5625em; line-height: 1.4; margin: 1.6em 0 .64em; }
  .as-h3 { font-size: 1.25em; font-weight: 400; letter-spacing: -.01em; line-height: 1.5; margin: 1.6em 0 .8em; }
  .as-h4 { font-weight: 700; letter-spacing: -.01em; margin: 1em 0; }
  .as-h5, .as-h6 { color: var(--md-default-fg-color--light); font-size: .8em; font-weight: 700; letter-spacing: -.01em; margin: 1.25em 0; }
</style>

# What is __Markdown__?

__Markdown is a way to write content for the web.__

It's written in what people call "plaintext", which is exactly the sort of text you're used to writing and seeing. Plaintext is just the regular alphabet with a few familiar symbols, like asterisks ( \* ) and backticks ( \` ).

Unlike cumbersome word processing applications, text written in Markdown can be easily shared between computers, mobile phones, and people.

__Formatting text in Markdown has a very gentle learning curve.__

## If you have ten minutes, you can learn Markdown! { #learn-markdown data-toc-label='Learn Markdown!' }

---

!!! tip
    In these lessons, you'll notice some `formatted monospace text`; this text is actually written in Markdown! Regular Markdown doesn't look any different than regular text, but we're providing some highlighting to make it easier to see.

### Italics and Bold

We'll start by learning two basic elements in text formatting: *italics* and __bold__.

To make a phrase *italic* in Markdown, you can surround words with an asterisk (`*`). For example, `*this*` word would become *italic*.

Similarly, to make phrases __bold__ in Markdown, you can surround words with two underscores (`__`). This will `__really__` get your point across.

Of course, you can use `*both italics and bold*` in the same line. You can also span them `__across multiple words__`.

In general, it doesn't matter which order you place the asterisks or underscores. To make the words "This is unbelievable" both bold and italic, like `*__"This is unbelievable"__*`. We'll place the asterisks `*__on the outside__*`, just to make it more legible.

### Headers

Let's take a look at another formatting convention: the header. Headers are frequently used on websites, magazine articles, and notices, to draw attention to a section. As their name implies, they act like titles or subtitles above sections.

There are six types of headers, in decreasing sizes:

??? tldr "Example"
    === "Level 1"
        <div class="as-h1">This is header one</div>
    === "Level 2"
        <div class="as-h2">This is header two</div>
    === "Level 3"
        <div class="as-h3">This is header three</div>
    === "Level 4"
        <div class="as-h4">This is header four</div>
    === "Level 5"
        <div class="as-h5">This is header five</div>
    === "Level 6"
        <div class="as-h6">This is header six</div>
    === "All Levels"
        <div class="as-h1">This is header one</div>
        <div class="as-h2">This is header two</div>
        <div class="as-h3">This is header three</div>
        <div class="as-h4">This is header four</div>
        <div class="as-h5">This is header five</div>
        <div class="as-h6">This is header six</div>
    === "Example Code"
        ```html
        #This is header one
        ##This is header two
        ###This is header three
        ####This is header four
        #####This is header five
        ######This is header six
        ```

To make headers in Markdown, you preface the phrase with a hash mark (`#`). You place the same number of hash marks as the size of the header you want. For example, for a header one, you'd use one hash mark (`# Header One`), while for a header three, you'd use three (`### Header Three`).

It's up to you to decide when it's appropriate to use which header. In general, headers one and six should be used sparingly.

### Links

We'll now learn how to make links to other web sites on the world wide web.

There are two different link types in Markdown, but both of them render the exact same way. The first link style is called an *inline link*. To create an inline link, you wrap the link text in brackets (`[ ]`), and then you wrap the link in parenthesis (`( )`). For example, to create a hyperlink to www.github.com, with a link text that says, Visit GitHub!, you'd write this in Markdown: `[Visit GitHub!](https://www.github.com)`.

You can add emphasis to link texts, if you like. You'll want to make sure that the bold phrasing occurs within the link text brackets and although it might make for an awkward experience, you can make links within headings, too.

That's really all there is to writing inline links.

The other link type is called a reference link. As the name implies, the link is actually a reference to another place in the document.

Here's an example of what we mean:

```markdown
     Here's [a link to something else][another place].
     Here's [yet another link][another-link].
     And now back to [the first link][another place].

     [another place]: www.github.com
     [another-link]: www.google.com
```

The "references" above are the second set of brackets: `[another place]` and `[another-link]`. At the bottom of a Markdown document, these brackets are defined as proper links to outside websites. An advantage of the reference link style is that multiple links to the same place only need to be updated once. For example, if we decide to make all of the `[another place]` links go somewhere else, we only have to change the single reference link.

Reference links don't appear in the rendered Markdown. You define them by providing the same tag name wrapped in brackets, followed by a colon, followed by the link.

### Images

If you know how to create links in Markdown, you can create images, too. The syntax is nearly the same.

Images also have two styles, just like links, and both of them render the exact same way. The difference between links and images is that images are prefaced with an exclamation point (`!`).

The first image style is called an *inline image link*. To create an inline image link, enter an exclamation point (`!`), wrap the alt text in brackets (`[ ]`), and then wrap the link in parenthesis (`( )`). (Alt text is a phrase or sentence that describes the image for the visually impaired.)

For example, to create an inline image link to https://octodex.github.com/images/bannekat.png, with an alt text that says, Benjamin Bannekat, you'd write this in Markdown: `![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png)`.

??? tldr "Example"
    === "Result"
        ![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png)

    === "Markdown"
        ```markdown
        ![Benjamin Bannekat](https://octodex.github.com/images/bannekat.png)
        ```

Although you don't *need* to add alt text, it will make your content accessible to your audience, including people who are visually impaired, use screen readers, or do not have high speed internet connections.

For a reference image, you'll follow the same pattern as a reference link. You'll precede the Markdown with an exclamation point, then provide two brackets for the alt text, and then two more for the image tag, like this: `![The founding father][Father]` At the bottom of your Markdown page, you'll define an image for the tag, like this: `[Father]: http://octodex.github.com/images/founding-father.jpg`.

Ta da! You've learned all there is to adding images in Markdown!

### Blockquotes

If you need to call special attention to a quote from another source, or design a pull quote for a magazine article, then Markdown's blockquote syntax will be useful. A blockquote is a sentence or paragraph that's been specially formatted to draw attention to the reader. For example:

> "The sin of doing nothing is the deadliest of all the seven sins. It has been said that for evil men to accomplish their purpose it is only necessary that good men should do nothing."

To create a block quote, all you have to do is preface a line with the "greater than" caret (`>`). For example:

```markdown
> In a few moments he was barefoot, his stockings folded in his pockets and his
  canvas shoes dangling by their knotted laces over his shoulders and, picking a
  pointed salt-eaten stick out of the jetsam among the rocks, he clambered down
  the slope of the breakwater.
```

You can also place a caret character on each line of the quote. This is particularly useful if your quote spans multiple paragraphs. For example:

```markdown
> His words seemed to have struck some deep chord in his own nature. Had he spoken
of himself, of himself as he was or wished to be? Stephen watched his face for some
moments in silence. A cold sadness was there. He had spoken of himself, of his own
loneliness which he feared.
>
> —Of whom are you speaking? Stephen asked at length.
>
> Cranly did not answer.
```

Notice that even blank lines must contain the caret character. This ensures that the entire blockquote is grouped together.

Block quotes can contain other Markdown elements, such as italics, images, or links.

??? tldr "Example"
    === "Result"
        > *Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts
        > of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and
        > maintenance are considered. We should forget about small efficiencies, say about 97% of the time: __premature 
        > optimization is the root of all evil__. Yet we should not pass up our opportunities in that critical 3%.*
        > <div class="as-h4"> - Donald Knuth</div>

    === "Markdown"
        ```markdown
        > *Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts
        > of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and
        > maintenance are considered. We should forget about small efficiencies, say about 97% of the time: __premature 
        > optimization is the root of all evil__. Yet we should not pass up our opportunities in that critical 3%.*
        > #### - Donald Knuth
        ```

Ta da! You've learned all there is to creating blockquotes in Markdown!

### Lists

There are two types of lists in the known universe: unordered and ordered. That's a fancy way of saying that there are lists with bullet points, and lists with numbers.

To create an unordered list, you'll want to preface each item in the list with an asterisk (`*`). Each list item also gets its own line. For example, a grocery list in Markdown might look like this:

```markdown
* Milk
* Eggs
* Salmon
* Butter
```

This Markdown list would render into the following bullet points:

* Milk
* Eggs
* Salmon
* Butter

Now, let's talk about ordered ones.

An ordered list is prefaced with numbers, instead of asterisks. Take a look at this recipe:

1. Crack three eggs over a bowl
2. Pour a gallon of milk into the bowl
3. Rub the salmon vigorously with butter
4. Drop the salmon into the egg-milk bowl

To write that in Markdown, you'd do this:

```markdown
1. Crack three eggs over a bowl
2. Pour a gallon of milk into the bowl
3. Rub the salmon vigorously with butter
4. Drop the salmon into the egg-milk bowl
```

Easy, right? It's just like you'd expect a list to look.

You can choose to add italics, bold, or links within lists, as you might expect.

* Azalea (*Ericaceae Rhododendron*)
* Chrysanthemum (*Anthemideae Chrysanthemum*)
* Dahlia (*Coreopsideae Dahlia*)

Occasionally, you might find the need to make a list with more depth, or, to nest one list within another. Have no fear, because the Markdown syntax is exactly the same. All you have to do is to remember to indent each asterisk one space more than the preceding item.

For example, in the following list, we're going to add some sub-lists to each "main" list item, describing the people in detail:

```markdown
* Tintin
    * A reporter
    * Has poofy orange hair
    * Friends with the world's most awesome dog
* Haddock
    * A sea captain
    * Has a fantastic beard
    * Loves whiskey
        * Possibly also scotch?
```

When rendered, this list turns into the following grouping:

* Tintin
    * A reporter
    * Has poofy orange hair
    * Friends with the world's most awesome dog
* Haddock
    * A sea captain
    * Has a fantastic beard
    * Loves whiskey
        * Possibly also scotch?

While you could continue to indent and add sub-lists indefinitely, it's usually a good idea to stop after three levels; otherwise, your text becomes a mess.

There's one more trick to lists and indentation that we'll explore, and that deals with the case of paragraphs. Suppose you want to create a bullet list that requires some additional context (but not another list). For example, it might look like this:

1. Crack three eggs over a bowl.

    Now, you're going to want to crack the eggs in such a way that you don't make a mess.

    If you _do_ make a mess, use a towel to clean it up!

2. Pour a gallon of milk into the bowl.

    Basically, take the same guidance as above: don't be messy, but if you are, clean it up!

3. Rub the salmon vigorously with butter.

    By "vigorous," we mean a strictly vertical motion. Julia Child once quipped:
    > Up and down and all around, that's how butter on salmon goes.

4. Drop the salmon into the egg-milk bowl.

    Here are some techniques on salmon-dropping:

    * Make sure no trout or children are present
    * Use both hands
    * Always have a towel nearby in case of messes

To create this sort of text, your paragraph must start on a line all by itself underneath the bullet point, and it must be indented by at least one space. For example, the list above looks like this in Markdown:

```markdown
1. Crack three eggs over a bowl.

    Now, you're going to want to crack the eggs in such a way that you don't make a mess.

    If you _do_ make a mess, use a towel to clean it up!

2. Pour a gallon of milk into the bowl.

    Basically, take the same guidance as above: don't be messy, but if you are, clean it up!

3. Rub the salmon vigorously with butter.

    By "vigorous," we mean a strictly vertical motion. Julia Child once quipped:
    > Up and down and all around, that's how butter on salmon goes.

4. Drop the salmon into the egg-milk bowl.

    Here are some techniques on salmon-dropping:

    * Make sure no trout or children are present
    * Use both hands
    * Always have a towel nearby in case of messes
```

Notice that the first two items have a single space. This looks a bit odd, so you might want to indent properly to match the characters up (like items three and four). In these paragraphs, you can include all sorts of other Markdown elements, like blockquotes, or even other lists!

You now know how to make lists in Markdown!

### Paragraphs

Markdown has several ways of formatting paragraphs.

Let's take a few lines of poetry as an example. Suppose you want to write text that looks like this:

> Do I contradict myself?  
> Very well then I contradict myself,  
> (I am large, I contain multitudes.)

Now, you might think that simply typing each verse onto its own line would be enough to solve the problem:

```markdown
Do I contradict myself?
Very well then I contradict myself,
(I am large, I contain multitudes.)
```

Unfortunately, you'd be wrong! This Markdown would render simply as a single straight line:

> Do I contradict myself? Very well then I contradict myself, (I am large, I contain multitudes.).

If you forcefully insert a new line, you end up breaking the togetherness:

```markdown
Do I contradict myself?

Very well then I contradict myself,

(I am large, I contain multitudes.)
```

This is what's known as a *hard break*; what our poetry asks for is a *soft break*. You can accomplish this by inserting two spaces *after* each new line. This is not possible to see, since spaces are invisible, but it'd look something like this:

```markdown
Do I contradict myself?··
Very well then I contradict myself,··
(I am large, I contain multitudes.)
```

Each dot (`·`) represents a space on the keyboard.

Aside from formatting poetry, one of the common uses for these soft breaks is in formatting paragraphs in lists. Recall in the previous lesson that we inserted a new line for multiple paragraphs within a list.

Et voila! You now know how to make soft breaks in Markdown!

### Optional Extras

You've completed all the lessons!

Believe it or not, we've only *just begun* exploring what can be accomplished with Markdown. There are many "extended" implementations of Markdown that support formats like tables, definition lists, footnotes, and more. Because they're non-standard, they're not essential to learning the basics, as we've introduced here.

See below for even more Markdown-based extensions

---

[__Material for MkDocs Markdown Reference__][material-mkdoc]{ target='secondary' .external-link }
*Technical documentation that just works. Create a branded static site from a set of Markdown files to host the documentation of your project.* We use Material for MkDocs here in the `cs_tools` project. This allows us to do cool things like the admonishment callouts, footnotes, and content tabs - all in a markdown-esque format.


[material-mkdoc]: https://squidfunk.github.io/mkdocs-material/reference/abbreviations/
