// Copyright (C) 2015  Julián Urbano <urbano.julian@gmail.com>
// Distributed under the terms of the MIT License.

package ti;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Scanner;
import java.util.StringTokenizer;

/**
 * A processor to extract terms from HTML documents.
 */
public class HtmlProcessor implements DocumentProcessor {
	HashSet<String> stopwords = new HashSet<>();
	// P2

	/**
	 * Creates a new HTML processor.
	 *
	 * @param pathToStopWords the path to the file with stopwords, or {@code null} if stopwords are not filtered.
	 * @throws IOException if an error occurs while reading stopwords.
	 */
	public HtmlProcessor(File pathToStopWords) throws IOException {
		// P2
		// Load stopwords
		try {
			Scanner myReader = new Scanner(pathToStopWords);
			while (myReader.hasNextLine()) {
				String data = myReader.nextLine();
				stopwords.add(data);
			}
			myReader.close();
		} catch (FileNotFoundException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
	}

	/**
	 * {@inheritDoc}
	 */
	public Tuple<String, String> parse(String html) {
		// P2
		// Parse document
        Document doc_html = Jsoup.parse(html);
        String title = doc_html.title();
        String body = "";
        try{
			body = doc_html.body().text();
		}
        catch (Exception e){
        	body = "";
		}

        Tuple<String, String> result = new Tuple<String, String>(title, body);

		return result; // Return title and body separately
	}

	/**
	 * Process the given text (tokenize, normalize, filter stopwords and stemize) and return the list of terms to index.
	 *
	 * @param text the text to process.
	 * @return the list of index terms.
	 */
	public ArrayList<String> processText(String text)
	{
		ArrayList<String> terms = new ArrayList<>();

		// P2
		// Tokenizing, normalizing, stopwords, stemming, etc.
		ArrayList<String> tokens = tokenize(text);
		for(String term: tokens){
			String norm = normalize(term);
			if(!isStopWord(norm)){
				String stem = stem(norm);
				terms.add(stem);
			}
		}
		return terms;
	}

	/**
	 * Tokenize the given text.
	 *
	 * @param text the text to tokenize.
	 * @return the list of tokens.
	 */
	protected ArrayList<String> tokenize(String text) // TODO: Mirar si està fent bé per nums i símbols
	{
		ArrayList<String> tokens = new ArrayList<>();
		StringTokenizer tokenizer = new StringTokenizer(text, ",");

		// P2
		while (tokenizer.hasMoreTokens()) {
			tokens.add(tokenizer.nextToken());
		}
		return tokens;
	}

	/**
	 * Normalize the given term.
	 *
	 * @param text the term to normalize.
	 * @return the normalized term.
	 */
	protected String normalize(String text) {
		String normalized = text.toLowerCase();
		return normalized;
	}

	/**
	 * Checks whether the given term is a stopword.
	 *
	 * @param term the term to check.
	 * @return {@code true} if the term is a stopword and {@code false} otherwise.
	 */
	protected boolean isStopWord(String term) {
		return stopwords.contains(term);
	}

	/**
	 * Stem the given term.
	 *
	 * @param term the term to stem.
	 * @return the stem of the term.
	 */
	protected String stem(String term) {
		Stemmer stemmer = new Stemmer();
		for(char a : term.toCharArray()){
			stemmer.add(a);
		}
		return stemmer.toString();
	}
}
