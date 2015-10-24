__author__ = 'nazareno'

from lxml import etree
import pickle

def fast_iter(context, func, *args, **kwargs):
    """
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    count = 0
    for event, elem in context:
        count +=1
        func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if count % 5000 == 0:
            print str(count) + " processed"
    del context

def process_element(elem, f):
    #print str(elem.xpath( 'released/text()'))
    country = elem.xpath( 'country/text()')
    styles = elem.xpath( 'styles/style/text()')
    if len(country) > 0 and country[0] == "Brazil" and \
        len(styles) > 0 and 'Samba' in styles:
        print "one more: "
        print elem.xpath( 'artists/artist/name/text()')
        result = formatXML(elem)
        #f.write(result + "\n")
        pickle.dump(result, f)

def formatXML(node):
    """
    Recursive operation which returns a tree formated
    as dicts and lists.
    Decision to add a list is to find the 'List' word
    in the actual parent tag.
    """
    ret = {}
    if node.items():
        ret.update(dict(node.items()))

    if node.text:
        ret['__content__'] = node.text

    for element in node:
        if element.tag not in ret:
            ret[element.tag] = []
        ret[element.tag].append(formatXML(element))

    # Flatten out any singletons
    for tag in ret:
        if isinstance(ret[tag], (list, tuple)) and len(ret[tag]) == 1:
            ret[tag] = ret[tag][0]

    if len(ret) == 1 and '__content__' in ret:
        return ret['__content__']

    return ret


if __name__ == '__main__':
    # tree = lxml.etree.parse(discogs_xml)
    context = etree.iterparse( "data/discogs_20151001_releases.xml", tag='release' )
    f = open('our-releases.pickle', 'w')
    fast_iter(context, process_element, f)
    f.close()