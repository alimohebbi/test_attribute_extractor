package com.moonpi.swiftnotes;


import android.support.test.espresso.DataInteraction;
import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onData;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.action.ViewActions.click;
import static android.support.test.espresso.action.ViewActions.closeSoftKeyboard;
import static android.support.test.espresso.action.ViewActions.replaceText;
import static android.support.test.espresso.action.ViewActions.scrollTo;
import static android.support.test.espresso.assertion.ViewAssertions.matches;
import static android.support.test.espresso.matcher.ViewMatchers.isDisplayed;
import static android.support.test.espresso.matcher.ViewMatchers.withClassName;
import static android.support.test.espresso.matcher.ViewMatchers.withContentDescription;
import static android.support.test.espresso.matcher.ViewMatchers.withId;
import static android.support.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class SwiftNotesTest1 {

    @Rule
    public ActivityTestRule<MainActivity> mActivityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void swiftNotesTest1() {
        ViewInteraction appCompatImageButton = onView(
                allOf(withId(R.id.newNote), withContentDescription("New note"),
                        childAtPosition(
                                childAtPosition(
                                        withId(android.R.id.content),
                                        0),
                                2),
                        isDisplayed()));
        appCompatImageButton.perform(click());

        ViewInteraction appCompatEditText = onView(
                allOf(withId(R.id.titleEdit),
                        childAtPosition(
                                allOf(withId(R.id.relativeLayoutEdit),
                                        childAtPosition(
                                                withId(android.R.id.content),
                                                0)),
                                1),
                        isDisplayed()));
        appCompatEditText.perform(replaceText("Title1"), closeSoftKeyboard());

        ViewInteraction appCompatEditText2 = onView(
                allOf(withId(R.id.bodyEdit),
                        childAtPosition(
                                allOf(withId(R.id.scrollView),
                                        childAtPosition(
                                                withId(R.id.relativeLayoutEdit),
                                                2)),
                                0)));
        appCompatEditText2.perform(replaceText("Note1"), closeSoftKeyboard());

        ViewInteraction appCompatImageButton2 = onView(
                allOf(childAtPosition(
                        allOf(withId(R.id.toolbarEdit),
                                childAtPosition(
                                        withId(R.id.relativeLayoutEdit),
                                        0)),
                        0),
                        isDisplayed()));
        appCompatImageButton2.perform(click());

        ViewInteraction appCompatButton = onView(
                allOf(withId(android.R.id.button1), withText("Yes"),
                        childAtPosition(
                                childAtPosition(
                                        withClassName(is("android.widget.ScrollView")),
                                        0),
                                3)));
        appCompatButton.perform(click());

        ViewInteraction textView = onView(
                allOf(withId(R.id.titleView), withText("Title1"),
                        childAtPosition(
                                allOf(withId(R.id.relativeLayout),
                                        childAtPosition(
                                                withId(R.id.listView),
                                                0)),
                                0),
                        isDisplayed()));
        textView.check(matches(withText("Title1")));

        ViewInteraction textView1 = onView(
                allOf(withId(R.id.bodyView), withText("Note1"),
                        childAtPosition(
                                allOf(withId(R.id.relativeLayout),
                                        childAtPosition(
                                                withId(R.id.listView),
                                                0)),
                                1),
                        isDisplayed()));
        textView1.check(matches(withText("Note1")));

    }

    private static Matcher<View> childAtPosition(
            final Matcher<View> parentMatcher, final int position) {

        return new TypeSafeMatcher<View>() {
            @Override
            public void describeTo(Description description) {
                description.appendText("Child at position " + position + " in parent ");
                parentMatcher.describeTo(description);
            }

            @Override
            public boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                return parent instanceof ViewGroup && parentMatcher.matches(parent)
                        && view.equals(((ViewGroup) parent).getChildAt(position));
            }
        };
    }
}
