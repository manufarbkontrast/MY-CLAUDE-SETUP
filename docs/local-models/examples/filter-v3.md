# filter-v3

## Ziel
filterProducts robust gegen echte Shopify-Daten machen und um maxStock erweitern.

## Dateien
- src/filter.js (ändern)
- test/filter.pinned.test.js (neu, Inhalt exakt wie unten)
- test/filter.test.js (darf ergänzt werden)

## Schritte
1. Signatur `filterProducts(products, options = {})`, danach `const { minPrice, maxPrice, minStock, maxStock } = options;`.
2. Wenn `products` kein Array ist: `throw new TypeError('products must be an array')`.
3. Preis mit `Number(p.price)` umwandeln. Ist das Ergebnis NaN und ist minPrice oder maxPrice gesetzt, wird das Produkt ausgeschlossen.
4. Filter `maxStock` ergänzen (`p.inventory <= maxStock`).
5. `test/filter.pinned.test.js` exakt mit dem Code aus „Vorgegebene Tests“ anlegen.

## Akzeptanzkriterien
- Alle Tests in test/filter.pinned.test.js und test/filter.test.js sind grün.
- Die Eingabe wird nicht verändert.

## Vorgegebene Tests
Datei test/filter.pinned.test.js, wörtlich übernehmen, NICHT ändern:

```js
const test = require('node:test');
const assert = require('node:assert');
const { filterProducts } = require('../src/filter');

const PRODUKTE = [
  { id: 1, title: 'Tasse',   price: '12.50', inventory: 3 },
  { id: 2, title: 'Poster',  price: 8,       inventory: 0 },
  { id: 3, title: 'Hoodie',  price: '49.90', inventory: 15 },
  { id: 4, title: 'Sticker', price: 'abc',   inventory: 100 },
];
const ids = list => list.map(p => p.id);

test('pinned: ohne options kommt alles zurück', () => {
  assert.deepStrictEqual(ids(filterProducts(PRODUKTE)), [1, 2, 3, 4]);
});
test('pinned: minPrice mit String-Preisen, ungültiger Preis fliegt raus', () => {
  assert.deepStrictEqual(ids(filterProducts(PRODUKTE, { minPrice: 10 })), [1, 3]);
});
test('pinned: maxPrice', () => {
  assert.deepStrictEqual(ids(filterProducts(PRODUKTE, { maxPrice: 10 })), [2]);
});
test('pinned: minStock + maxStock', () => {
  assert.deepStrictEqual(ids(filterProducts(PRODUKTE, { minStock: 1, maxStock: 10 })), [1]);
});
test('pinned: minPrice + maxStock kombiniert', () => {
  assert.deepStrictEqual(ids(filterProducts(PRODUKTE, { minPrice: 5, maxStock: 20 })), [1, 2, 3]);
});
test('pinned: TypeError bei Nicht-Array', () => {
  assert.throws(() => filterProducts(null), TypeError);
});
test('pinned: Eingabe bleibt unverändert', () => {
  const kopie = structuredClone(PRODUKTE);
  filterProducts(PRODUKTE, { minPrice: 10, maxStock: 5 });
  assert.deepStrictEqual(PRODUKTE, kopie);
});
```

## Nicht tun
- test/filter.pinned.test.js nach dem Anlegen nicht mehr ändern.
- Keine neuen Abhängigkeiten, kein TypeScript, keine anderen Dateien ändern.

test_command: node --test
