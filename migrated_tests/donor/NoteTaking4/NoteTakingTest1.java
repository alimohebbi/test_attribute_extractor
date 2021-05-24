package chan.android.app.pocketnote;


import android.support.test.espresso.DataInteraction;
import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onData;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.pressBack;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.action.ViewActions.*;
import static android.support.test.espresso.assertion.ViewAssertions.*;
import static android.support.test.espresso.matcher.ViewMatchers.*;

import chan.android.app.pocketnote.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.is;
@LargeTest
@RunWith(AndroidJUnit4.class)
public class NoteTakingTest1 {

    @Rule
    public ActivityTestRule<MainActivity> mActivityTestRule = new ActivityTestRule<>(MainActivity.class);

    @Test
    public void noteTakingTest1() {
        ViewInteraction linearLayout = onView(
                allOf(withId(R.id.notes_$_linearlayout_empty),
                        childAtPosition(
                                allOf(withId(R.id.notes_$_viewflipper),
                                        childAtPosition(
                                                withClassName(is("android.widget.RelativeLayout")),
                                                0)),
                                2),
                        isDisplayed()));
        linearLayout.perform(click());

        ViewInteraction editText1 = onView(
                allOf(withId(R.id.editor_$_edittext_title),
                        childAtPosition(
                                allOf(withId(R.id.editor_$_linearlayout_border),
                                        childAtPosition(
                                                withClassName(is("android.widget.LinearLayout")),
                                                0)),
                                0),
                        isDisplayed()));
        editText1.perform(replaceText("to-do"), closeSoftKeyboard());

        ViewInteraction noteEditor2 = onView(
                allOf(withId(R.id.editor_$_note_editor),
                        childAtPosition(
                                childAtPosition(
                                        withId(android.R.id.content),
                                        0),
                                1),
                        isDisplayed()));
        noteEditor2.perform(replaceText("Go shopping"), closeSoftKeyboard());

        pressBack();

        ViewInteraction textView = onView(
                allOf(withId(R.id.note_item_$_textview_title), withText("to-do"),
                        childAtPosition(
                                allOf(withId(R.id.note_item_$_parent),
                                        childAtPosition(
                                                withId(R.id.notes_$_listview),
                                                0)),
                                1),
                        isDisplayed()));
        textView.check(matches(withText("to-do")));

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
